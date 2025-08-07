import os
from dotenv import load_dotenv
from flask import Flask, render_template, request
import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from google import genai
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in one sentence."
)

print(response.text)

# 3) Prediction helper
def bert_predict_proba(texts):
    if isinstance(texts, np.ndarray):
        texts = texts.tolist()
    if isinstance(texts, str):
        texts = [texts]
    enc = tokenizer(
        texts,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=512
    ).to(device)
    with torch.no_grad():
        logits = model(**enc).logits
    return F.softmax(logits, dim=1).cpu().numpy()

# 4) Flask app
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    result = confidence = alert_class = explanation = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form.get("email", "").strip()
        if email_text:
            # get prediction
            probs = bert_predict_proba(email_text)[0]
            label = int(np.argmax(probs))
            confidence = round(probs[label] * 100, 2)
            result = "Spam" if label == 1 else "Not Spam"
            alert_class = "alert alert-danger" if label == 1 else "alert alert-success"

            # moderate-confidence override
            if 40 <= confidence <= 60:
                alert_class = "alert alert-warning"
                result = "Likely " + result

            # call Gemini to explain the decision
            prompt = (
                f"Explain in plain English why a BERT-based spam detector would "
                f"classify the following email as “{result}”:\n\n\"\"\"\n{email_text}\n\"\"\""
            )
            try:
                resp = gemini_client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                explanation = resp.text.strip()
            except Exception as e:
                explanation = f"Error generating explanation: {e}"

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        alert_class=alert_class,
        email_text=email_text,
        explanation=explanation
    )

if __name__ == "__main__":
    app.run(debug=True)