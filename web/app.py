from flask import Flask, render_template, request
from markupsafe import Markup
import joblib
import shap
import numpy as np
import pandas as pd
import re

app = Flask(__name__)

# 1) Load your sklearn pipeline
model      = joblib.load("./output/models/LogisticRegression_tfidf.joblib")
vectorizer = model.named_steps['vectorizer']   # or 'vectorizer'
classifier = model.named_steps['classifier']

# 2) Build a small numeric background for KernelExplainer
df = pd.read_csv("./data/analysis/emails_augmented.csv")
assert 'body_no_stopwords' in df.columns and 'label' in df.columns

texts  = df['body_no_stopwords'].tolist()
X_full = vectorizer.transform(texts).toarray()

# sample up to 100 rows for background
rng    = np.random.RandomState(42)
idx    = rng.choice(X_full.shape[0], min(100, X_full.shape[0]), replace=False)
background = X_full[idx]

# 3) Wrap predict_proba in a plain numpy→numpy function
def model_proba(x: np.ndarray) -> np.ndarray:
    # x is (n_samples, n_features)
    return classifier.predict_proba(x)

# 4) Instantiate a KernelExplainer
explainer = shap.KernelExplainer(model_proba, background)

# 5) Helper to highlight the top‐k shap words in your raw email
def highlight_text(email_text: str,
                   shap_vals: np.ndarray,
                   vectorizer,
                   top_n: int = 5) -> Markup:
    """
    email_text: the original string
    shap_vals : 1D array of length = n_features (for spam class)
    """
    try:
        feature_names = vectorizer.get_feature_names_out()
    except:
        feature_names = vectorizer.get_feature_names()

    # DEBUG: Print all feature names (first 10 for brevity)
    print("DEBUG: feature_names example:", feature_names[:10])

    # Pick the top_n features by absolute SHAP value
    top_idxs  = np.argsort(np.abs(shap_vals))[-top_n:]
    important = { feature_names[i] for i in top_idxs if shap_vals[i] != 0 }
    print("DEBUG: Important features chosen by SHAP:", important)

    # DEBUG: Let's show the email text
    print("DEBUG: email_text:", email_text)

    # For testing: Uncomment to force highlighting a real token:
    # important = {"test", "money"} # Add words you know are in your email

    def repl(m):
        w = m.group(0)
        # All lowercase match, but use original casing for output
        return f'<span class="highlight">{w}</span>' if w.lower() in important else w

    highlighted = re.sub(r'\b\w+\b', repl, email_text, flags=re.IGNORECASE)

    # DEBUG: Print the highlighted HTML markup fragment
    print("DEBUG: highlighted_email fragment:", highlighted[:500]) # first 500 chars

    return Markup(highlighted)

# 6) Flask endpoint
@app.route("/", methods=["GET", "POST"])
def index():
    result           = None
    confidence       = None
    alert_class      = None
    highlighted_email = ""
    email_text       = ""

    if request.method == "POST":
        email_text = request.form.get("email", "").strip()

        if email_text:
            # vectorize new email
            x_vec = vectorizer.transform([email_text]).toarray()

            # predict
            p_not, p_spam = classifier.predict_proba(x_vec)[0]
            if p_spam >= 0.5:
                result     = "Spam"
                confidence = round(p_spam * 100, 2)
            else:
                result     = "Not Spam"
                confidence = round((1 - p_spam) * 100, 2)

            # choose alert style
            if 40 <= confidence <= 60:
                alert_class = "alert alert-warning"
                result      = "Likely " + result
            else:
                alert_class = "alert alert-danger" if result == "Spam" else "alert alert-success"

            # get SHAP values
            shap_vals = explainer.shap_values(x_vec, nsamples=100)
            print("DEBUG: shap_vals type:", type(shap_vals), "shape:", getattr(shap_vals, 'shape', None))

            # If it's a numpy array (should be for binary): shape (1, n_features, 2)
            if isinstance(shap_vals, np.ndarray):
                # (n_samples, n_features, n_classes)
                # For first (only) sample, all features, class 1 ("spam")
                shap_for_spam = shap_vals[0, :, 1]
            elif isinstance(shap_vals, list) and len(shap_vals) > 1:
                # multiclass fallback: use class 1
                shap_for_spam = shap_vals[1][0]
            elif isinstance(shap_vals, list):
                shap_for_spam = shap_vals[0][0]
            else:
                raise RuntimeError("Unexpected type/shape for SHAP values")

            # highlight top words
            highlighted_email = highlight_text(
                email_text,
                shap_for_spam,
                vectorizer,
                top_n=5
            )

            # DEBUG: print highlighted_email to terminal
            print("DEBUG: highlighted_email passed to template:\n", highlighted_email)

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        email_text=email_text,
        highlighted_email=highlighted_email,
        alert_class=alert_class,
    )

if __name__ == "__main__":
    app.run(debug=True)