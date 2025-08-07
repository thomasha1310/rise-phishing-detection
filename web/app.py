import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

import torch
import torch.nn.functional as F
import numpy as np
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# “Old” GenAI client:
from google import genai

# 1) Load .env & init Gemini client
load_dotenv()  
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env file")

gemini_client = genai.Client(api_key=api_key)

# 2) Load BERT model & tokenizer
MODEL_DIR = "output/models/phishing-bert-model"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    MODEL_DIR, local_files_only=True
).to(device).eval()

def bert_predict_proba(texts):
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

# 3) Flask app
app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    result = confidence = alert_class = explanation = None
    email_text = ""

    if request.method == "POST":
        email_text = request.form.get("email", "").strip()
        if email_text:
            # BERT predict
            probs = bert_predict_proba(email_text)[0]
            label = int(np.argmax(probs))
            confidence = round(probs[label] * 100, 2)
            result = "Spam" if label == 1 else "Not Spam"
            alert_class = "alert alert-danger" if label == 1 else "alert alert-success"

            # moderate‐confidence override
            if 40 <= confidence <= 60:
                alert_class = "alert alert-warning"
                result = "Likely " + result

            # Gemini explanation (old API)
            prompt = (
                f"""The following message was flagged as “{result}”.
                Explain in around two sentences why it is most likely a "{result}" message as well as what it is targeting out of the user if it is a spam email.
                Provide a 1-2 sentence suggestion on what the recipient should do next.
                Direct all messages as if you are speaking directly to the recipient of the email"
                f"\n\n"
                f"\"\"\"\n{email_text}\n\"\"\""""
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
    # make sure you’re in the venv with google-genai installed
    app.run(debug=True)