# ========== IMPORTS ==========

import pandas as pd
import re
import tldextract
import nltk
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# ========== NLTK INITIALIZATION ==========

print("Preparing NLTK...")
nltk.download('punkt', download_dir='nltk_data')
nltk.download('punkt_tab', download_dir='nltk_data')
nltk.download('wordnet', download_dir='nltk_data')
nltk.download('omw-1.4', download_dir='nltk_data')
nltk.download('stopwords', download_dir='nltk_data')
nltk.data.path.append('./nltk_data')
lemmatizer = WordNetLemmatizer()

# ========== READ DATA ==========

print("Reading data...")
df = pd.read_csv('./data/analysis/emails.csv')

# ========== CONSTANTS ==========

URL_PATTERN = r'https?:\/\/[^\s<>"]+|[^\s<>"]+\.[A-Za-z]{1,2}[^\s<>"]+'

GENERAL_REDIRECTS = {
    'bit.ly', 'tinyurl.com', 'ow.ly', 'rebrand.ly', 'is.gd',
    'buff.ly', 'adf.ly', 'shorte.st', 'cutt.ly', 'clk.im',
    'yellkey.com', 'v.gd'
}

URGENT_KEYWORDS = {
    'urgent', 'immediately', 'important', 'action', 'required', 'asap',
    'alert', 'verify', 'warning', 'account', 'suspend', 'suspended',
    'locked', 'security', 'update', 'login', 'log-in', 'expire',
    'expiration', 'failure', 'failed', 'unauthorized', 'breach',
    'verify', 'attention', 'risk', 'click', 'now', 'respond', 'response',
    'confirm', 'confirmation', 'access', 'limited', 'final', 'notice',
    'deadline', 'deactivation', 'reactivate', 'validate', 'critical',
    'problem', 'issue', 'payment', 'invoice', 'bill', 'charge', 'refund',
    'dispute', 'settlement', 'penalty', 'compliance', 'legal', 'violation'
}

STOP_WORDS = set(stopwords.words('english'))

# ========== METHODS ==========

def extract_urls(text: str) -> list:
    if not isinstance(text, str):
        return []
    return re.findall(URL_PATTERN, text)

def count_urls(text: str) -> int:
    if not isinstance(text, str):
        return 0
    return len(re.findall(URL_PATTERN, text))
    
def get_domain(url: str) -> str:
    ext = tldextract.extract(url)
    if ext.domain and ext.suffix:
        return f"{ext.domain}.{ext.suffix}"
    return None

def count_urgent_words(text):
    tokens = word_tokenize(str(text).lower())
    lemmas = [lemmatizer.lemmatize(word) for word in tokens]
    return sum(1 for word in lemmas if word in URGENT_KEYWORDS)


print("Processing data...")

# ========== TOTAL URLS ==========

print("Counting URLs...")
df['num_urls'] = df.apply(
    lambda row: count_urls(row['subject']) + count_urls(row['body']),
    axis=1
)

# ========== REDIRECTS ==========

print("Counting redirects...")
df['num_redirects'] = df.apply(
    lambda row: sum(
        1 for url in extract_urls(str(row['subject']) + ' ' + str(row['body']))
        if (lambda ext: f"{ext.domain}.{ext.suffix}")(tldextract.extract(url)) in GENERAL_REDIRECTS
    ),
    axis=1
)

# ========== WORD COUNT ==========

print("Counting words...")
df['num_words'] = df.apply(
    lambda row: len(str(row['body']).split()),
    axis=1
)

# ========== NON-ASCII CHARS ==========

print("Counting non-ASCII characters...")
df['num_chars_foreign'] = df.apply(
    lambda row: sum(1 for char in str(row['body']) if not char.isascii()),
    axis=1
)

# ========== SPECIAL CHARS ==========

print("Counting special characters...")
df['num_chars_special'] = df.apply(
    lambda row: sum(1 for char in str(row['body']) if not char.isalnum() and not char.isspace()),
    axis=1
)

# ========== URGENCY ==========

print("Counting urgent words...")
df['num_urgent_words'] = df['body'].apply(count_urgent_words)

# ========== STOPWORDS COUNT ==========

print("Counting stopwords...")
df['num_stopwords'] = df['body'].apply(
    lambda row: sum(
        1 for word in word_tokenize(str(row).lower()) if word in STOP_WORDS
    )
)

# ========== NO STOPWORDS COLUMN ==========

print("Compiling no-stopwords column...")
df['body_no_stopwords'] = df['body'].apply(
    lambda row: ' '.join(
        word for word in word_tokenize(str(row).lower())
        if word.isalnum() and word not in STOP_WORDS
    )
)

# ========== EXPORT DATA ==========

print("Exporting data...")
df.to_csv('./data/analysis/emails_augmented.csv', index=False)
print("Done.")