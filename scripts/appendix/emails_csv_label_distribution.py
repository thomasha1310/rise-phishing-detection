import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('./data/analysis/emails.csv')

counts = df['label'].value_counts().sort_index()

fig = plt.figure(figsize=(4, 3), dpi=300)
ax = fig.add_subplot(1, 1, 1)

ax.bar(counts.index, counts.values, width=0.8)
ax.set_xticks([0.0, 1.0])
ax.set_title('Distribution of labels in emails.csv')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.grid(False)

fig.savefig("./output/appendix/emails_csv_label_distribution.png", bbox_inches='tight')

plt.show()
