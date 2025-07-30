# Data Appendix

This data appendix provides a complete definition of every variable in each of the analysis datasets. Summary statistics and basic distribution visualizations are also provided for quantitative variables.

## `emails.csv`

Each entry in this dataset represents a single email.

### `subject`

This field (`object` datatype) is the subject line of the email, usually indicating what the email is about.

### `body`

This field (`object` datatype) is the body of the email, containing most of the content sent to an end user.

### `label`

This field (`int` datatype) is an indication of whether an email is phishing or legitimate.

A label of `1` indicates that the email is phishing, while a `0` indicates that the email is legitimate.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/0f9f6863-a2e4-4d51-b6c8-a717d8544646" />

## `emails_augmented.csv`

The `subject`, `body`, and `label` fields are identical to those in `emails.csv`.

### `num_urls`

This field (`int` datatype) is an indication of the number of URLs that an email contains. A URL is defined as any string matching the following regular expression:
```regex
https?:\/\/[^\s<>"]+|[^\s<>"]+\.[A-Za-z]{1,2}[^\s<>"]+
```

<img width="500" alt="image" src="https://github.com/user-attachments/assets/3f307b46-ef4d-4576-ad58-2321807b7762" />

### `num_words`

This field (`int` datatype) is an indication of the number of words in an email body. This is obtained by counting the number of strings after splitting the `body` field on all whitespace characters (discarding empty strings).

<img width="500" alt="image" src="https://github.com/user-attachments/assets/f4c520b9-2f1f-4c61-9579-8100946ed65d" />

### `num_chars_foreign`

This field (`int` datatype) is an indication of the number of non-ASCII characters in an email body, defined using the Python built-in `isascii()` method.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/a4b3a00a-2d3c-459a-9f10-17e7ab65c532" />

### `num_chars_special`

This field (`int` datatype) is an indication of the number of special characters in an email body, defined as fulfilling neither the `isalnum()` nor the `isspace()` Python built-in methods.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/3726b6c4-41dd-4d56-adaa-add2dd301457" />

### `num_urgent_words`

This field (`int` datatype) is an indication of the number of urgent words in an email body. The email body is tokenized and lemmatized using NLTK, and the resulting words are matched against the following set of predefined urgent words:

```python
'urgent', 'immediately', 'important', 'action', 'required', 'asap',
'alert', 'verify', 'warning', 'account', 'suspend', 'suspended',
'locked', 'security', 'update', 'login', 'log-in', 'expire',
'expiration', 'failure', 'failed', 'unauthorized', 'breach',
'verify', 'attention', 'risk', 'click', 'now', 'respond', 'response',
'confirm', 'confirmation', 'access', 'limited', 'final', 'notice',
'deadline', 'deactivation', 'reactivate', 'validate', 'critical',
'problem', 'issue', 'payment', 'invoice', 'bill', 'charge', 'refund',
'dispute', 'settlement', 'penalty', 'compliance', 'legal', 'violation'
```

<img width="500" alt="image" src="https://github.com/user-attachments/assets/7d515311-601e-4f8b-8b1e-8c78c5f5b50b" />

### `num_stopwords`

This field (`int` datatype) is an indication of the number of stopwords in an email body. The email body is tokenized using NLTK, and the resulting words are matched against an NLTK corpus of predefined English stopwords.

<img width="500" alt="image" src="https://github.com/user-attachments/assets/46a4993d-f1c0-4891-b5cf-30be9ab87a0d" />

### `body_no_stopwords`

This field (`object` datatype) is obtained by tokenizing the email body, then concatenating all alphanumeric, non-stopword tokens (separated by spaces).

## `validate.csv`

