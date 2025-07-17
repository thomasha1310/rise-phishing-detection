# phishing_email_classifier.py

import os

output_dir = './generated'
os.makedirs(output_dir, exist_ok=True)

import pandas as pd
import numpy as np
import re
import string

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

import lime
import lime.lime_text
from sklearn.pipeline import make_pipeline

# ========== 1. Load Dataset ==========
df = pd.read_csv('./data/emails.csv')  # change path as needed
assert 'body' in df.columns and 'label' in df.columns, "Missing required columns."

# ========== 2. Text Preprocessing ==========
def clean_email(text):
    text = re.sub(r'<[^>]+>', '', text)  # remove HTML tags
    text = re.sub(r'http\S+', '', text)  # remove URLs
    text = re.sub(r'\d+', '', text)      # remove digits
    text = text.translate(str.maketrans('', '', string.punctuation))  # remove punctuation
    text = text.lower().strip()
    return text

df['clean_email'] = df['body'].astype(str).apply(clean_email)

# ========== 3. Vectorization ==========
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
X = vectorizer.fit_transform(df['clean_email'])
y = df['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ========== 4. Model Training ==========
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ========== 5. Evaluation ==========
y_pred = model.predict(X_test)
y_prob = model.predict_proba(X_test)
print("Classification Report:")
print(classification_report(y_test, y_pred))
print(y_prob)

# ========== 6. Interpretability ==========
# Feature Importance (Global)
feature_names = np.array(vectorizer.get_feature_names_out())
coefs = model.coef_[0]
top_phishing_idx = np.argsort(coefs)[-10:]
top_legit_idx = np.argsort(coefs)[:10]

print("\nTop indicative words for phishing:")
for word, coef in zip(feature_names[top_phishing_idx], coefs[top_phishing_idx]):
    print(f"{word}: {coef:.4f}")

print("\nTop indicative words for legitimate:")
for word, coef in zip(feature_names[top_legit_idx], coefs[top_legit_idx]):
    print(f"{word}: {coef:.4f}")

# ========== 7. Local Explanation with LIME ==========
# LIME needs raw text and a pipeline
raw_X_train, raw_X_test = train_test_split(df['clean_email'], test_size=0.2, random_state=42)

pipeline = make_pipeline(vectorizer, model)
explainer = lime.lime_text.LimeTextExplainer(class_names=['Legitimate', 'Phishing'])

# Pick a test email to explain
idx = 0
print("\nExplaining instance:", raw_X_test.iloc[idx])
exp = explainer.explain_instance(raw_X_test.iloc[idx], pipeline.predict_proba, num_features=10)

# Save as HTML
exp.save_to_file(os.path.join(output_dir, 'lime_explanation.html'))

# ========== 8. Save Model (Optional) ==========
import joblib
joblib.dump(model, './generated/phishing_model.pkl')
joblib.dump(vectorizer, './generated/tfidf_vectorizer.pkl')

print("\nModel and vectorizer saved.")
