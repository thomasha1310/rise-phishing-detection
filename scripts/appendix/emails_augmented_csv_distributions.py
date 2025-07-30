import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Load the data
print('Reading data...')
df = pd.read_csv('./data/analysis/emails_augmented.csv')

# Save summary statistics
print('Saving summary statistics...')
with open('./output/appendix/augmented_summary.txt', 'w') as f:
    f.write(df.describe().to_string())

# Ensure output directory exists
os.makedirs('./output/appendix', exist_ok=True)

# Fields to plot
fields = [
    ('num_urls', 'URLs'),
    ('num_words', 'word count'),
    ('num_chars_foreign', 'non-ASCII characters'),
    ('num_chars_special', 'special characters'),
    ('num_urgent_words', 'urgent words'),
    ('num_stopwords', 'stopwords')
]

print('Preparing violin plots...')
for item in fields:
    field = item[0]
    readable = item[1]
    log_field = f'log1p_{field}'
    df[log_field] = np.log1p(df[field])
    
    # ===== FULL DATASET =====
    fig = plt.figure(figsize=(4, 3), dpi=300)
    ax = fig.add_subplot(1, 1, 1)
    sns.violinplot(
        data = df,
        x='label',
        y=log_field,
        hue='label',
        ax=ax,
        inner='quartile',
        density_norm='width',
        palette='muted'
    )
    ax.get_legend().remove()
    ax.set_title(f'Distribution of {readable} (log1p)')
    ax.set_xlabel('Label')
    ax.set_ylabel(f'Log1p of {readable}')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(False)
    fig.savefig(f'./output/appendix/{field}_distribution', bbox_inches='tight')
    plt.close(fig)


print("Done.")
