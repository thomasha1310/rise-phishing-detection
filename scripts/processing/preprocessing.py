# ========== IMPORTS ==========

import pandas as pd
import random
import re

# ========== INITIALIZATION ==========

random.seed(12)

# ========== HANDLE ENRON DATA ==========

df_enron = pd.read_csv('./data/inputs/Enron.csv')
fortune = pd.read_csv('./data/inputs/fortune500.csv')
companies = fortune['company']
df_enron.info()
df_enron.head()

# ========== FUNCTIONS ==========

def replace_enron(text: str) -> str:
    """
    Replace all instances of the 'enron' (case-insensitive) with a randomly
    selected company from the list of Fortune 500 companies.
    """
    if not isinstance(text, str):
        return text
    return re.sub(r'enron', lambda _: random.choice(companies), text, flags=re.IGNORECASE)

# ========== REPLACE 'ENRON' ==========

text_columns = df_enron.select_dtypes(include='object').columns
for col in text_columns:
    df_enron[col] = df_enron[col].apply(replace_enron)


# ========== READ DATASETS ==========

df_ceas = pd.read_csv('./data/inputs/CEAS_08.csv')
df_ling = pd.read_csv('./data/inputs/Ling.csv')
df_nazario = pd.read_csv('./data/inputs/Nazario.csv')
df_nigerian = pd.read_csv('./data/inputs/Nigerian_Fraud.csv')
df_assassin = pd.read_csv('./data/inputs/SpamAssasin.csv')
df_trec = pd.read_csv('./datasets/TREC_07.csv')

# ========== DATASET INFO ==========

print('=============== CEAS 08  ===============')
df_ceas.info()
print('=============== ENRON    ===============')
df_enron.info()
print('=============== LING     ===============')
df_ling.info()
print('=============== NAZARIO  ===============')
df_nazario.info()
print('=============== NIGERIAN ===============')
df_nigerian.info()
print('=============== ASSASSIN ===============')
df_assassin.info()
print('=============== TREC_07  ===============')
df_trec.info()

# ========== TRIM COLUMNS ==========

df_trimmed_ceas = df_ceas[['subject', 'body', 'label']]
df_trimmed_enron = df_enron[['subject', 'body', 'label']]
df_trimmed_ling = df_ling[['subject', 'body', 'label']]
df_trimmed_nazario = df_nazario[['subject', 'body', 'label']]
df_trimmed_nigerian = df_nigerian[['subject', 'body', 'label']]
df_trimmed_assassin = df_assassin[['subject', 'body', 'label']]
df_trimmed_trec = df_trec[['subject', 'body', 'label']].copy()

print('=============== CEAS 08  ===============')
df_trimmed_ceas.info()
print('=============== ENRON    ===============')
df_trimmed_enron.info()
print('=============== LING     ===============')
df_trimmed_ling.info()
print('=============== NAZARIO  ===============')
df_trimmed_nazario.info()
print('=============== NIGERIAN ===============')
df_trimmed_nigerian.info()
print('=============== ASSASSIN ===============')
df_trimmed_assassin.info()

# ========== CONCATENATE ==========

df_complete = pd.concat(
    [df_trimmed_ceas,
     df_trimmed_enron,
     df_trimmed_assassin,
     df_trimmed_ling,
     df_trimmed_nazario,
     df_trimmed_nigerian],
    axis=0,
    ignore_index=True
)
df_complete.info()

# ========== REMOVE INVALID DATA ==========

df_complete.dropna(inplace=True)
df_complete.drop_duplicates(inplace=True)
df_complete.info()

df_trec.dropna(inplace=True)
df_trec.drop_duplicates(inplace=True)
df_trec.info()

# ========== COUNT PHISHING/LEGITIMATE ==========

print(df_complete['label'].value_counts())
print(df_trimmed_enron['label'].value_counts())
print(df_trimmed_trec['label'].value_counts())

# ========== EXPORT DATA ==========

df_complete.to_csv('./data/analysis/emails.csv', index=False)
df_trimmed_trec.to_csv('./data/analysis/validate.csv', index=False)