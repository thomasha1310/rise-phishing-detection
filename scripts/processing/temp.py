import pandas as pd

df = pd.read_csv('./data/analysis/emails_augmented.csv')

print(df.isnull().sum())

df.dropna(inplace=True)
print(df.isnull().sum())

df.to_csv('./data/analysis/emails_augmented.csv')