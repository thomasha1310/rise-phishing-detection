from flask import Flask, render_template, request
from markupsafe import Markup
import torch, torch.nn.functional as F, numpy as np, shap
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# 1) Load model/tokenizer locally
MODEL_DIR = "output/models/phishing-bert-model"
device    = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
model     = AutoModelForSequenceClassification.from_pretrained(
               MODEL_DIR, local_files_only=True
            ).to(device).eval()

# 2) Robust wrapper
def bert_predict_proba(texts):
    # ensure we only ever feed HF a Python list of str
    if isinstance(texts, np.ndarray):
        texts = texts.tolist()
    if isinstance(texts, str):
        texts = [texts]
    texts = [str(t) for t in texts]
    enc = tokenizer(texts, return_tensors="pt", padding=True,
                    truncation=True, max_length=512).to(device)
    with torch.no_grad():
        logits = model(**enc).logits
    return F.softmax(logits, dim=1).cpu().numpy()

# 3) SHAP explainer
explainer = shap.Explainer(
    bert_predict_proba,
    masker=shap.maskers.Text(tokenizer),
    output_names=["Not Spam","Spam"]
)

def highlight_text(email, shap_values, top_n=5):
    toks = shap_values.data[0]
    vals = shap_values.values[0][:,1]     # spam‐class
    idxs = np.argsort(np.abs(vals))[-top_n:]
    tops = {toks[i] for i in idxs}
    out = []
    for t in toks:
        esc = t.replace("<","&lt;").replace(">","&gt;")
        if t in tops:
            out.append(f'<span class="highlight">{esc}</span>')
        else:
            out.append(esc)
    return Markup(" ".join(out))

# 4) Flask app
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    result = confidence = alert_class = highlighted_email = None
    email_text = ""
    if request.method=="POST":
        email_text = request.form.get("email","").strip()
        if email_text:
            probs = bert_predict_proba(email_text)[0]
            label = int(np.argmax(probs))
            confidence = round(probs[label]*100,2)
            result = "Spam" if label==1 else "Not Spam"
            alert_class = (
              "alert alert-danger" if label==1
              else "alert alert-success"
            )
            if 40<=confidence<=60:
                alert_class = "alert alert-warning"
                result = "Likely "+result

            shap_vals = explainer([email_text], max_evals=50)
            highlighted_email = highlight_text(email_text, shap_vals, top_n=5)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        alert_class=alert_class,
        email_text=email_text,
        highlighted_email=highlighted_email
    )

if __name__=="__main__":
    app.run(debug=True)