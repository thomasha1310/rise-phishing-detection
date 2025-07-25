# PhishFence: Phishing Detection with Explainable AI

[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-orange)](https://lifecycle.r-lib.org/articles/stages.html)
[![license](https://img.shields.io/badge/license-MIT_|_CC_BY--SA_4.0-blue)](LICENSE.md)

## Repository Structure

```
phishfence/
├── .gitattributes
├── .gitignore
├── LICENSE.md
├── README.md
├── environment.txt
├── PhishFence.pdf
├── data/
│   ├── input/
│   │   ├── CEAS_08.csv
│   │   ├── Enron.csv
│   │   ├── Ling.csv
│   │   ├── Nazario.csv
│   │   ├── Nigerian_Fraud.csv
│   │   ├── SpamAssasin.csv
│   │   ├── TREC_07.csv
│   │   ├── fortune500.csv
│   │   └── metadata/
│   │       ├── SOURCES.md
│   │       └── CODEBOOKS.md
│   └── analysis/
│       ├── emails.csv
│       ├── emails_augmented.csv
│       ├── validate.csv
│       └── APPENDIX.md
├── scripts/
│   ├── processing/
│   │   ├── preprocessing.py
│   │   └── data_augmentation.py
│   ├── analysis/
│   │   └── Logistic_Regression.ipynb
│   └── main.py
└── output/
    └── results/
        └── ...
```

## Data

We used a variety of publicly available datasets. The raw data is contained within `phishfence/data/input`. The sources for the data are noted in [`phishfence/data/input/metadata/sources.md`](https://github.com/thomasha1310/rise-phishing-detection/blob/main/data/input/metadata/SOURCES.md).

### Pre-Processing

Since each dataset had different columns, we trimmed each dataset to include only the `subject`, `body`, and `label` columns. The six trimmed datasets were then concatenated to create a complete dataset.

All duplicate rows and rows with missing values were removed, and the dataset was exported as `emails.csv`. This processed dataset contains 82,138 entries, of which 39,527 (48%) are legitimate and 42,611 (52%) are malicious.

### Handling the Enron Corpus

After initial testing, we determined that the Enron corpus, consisting of 29,767 emails, comprised too large of a proportion (roughly 36%) of the total dataset. In particular, the word "Enron" consistently appeared as the top indicative word for legitimate emails, with a score of -11.0770.

To prevent overfitting to the Enron corpus, we replaced all instances of the word "Enron" in the `Enron.csv` with a randomly selected company from the Fortune 500 list of companies before recompiling the full dataset.

### Data Augmentation

In order to increase the training options available to us, we [augmented](https://github.com/thomasha1310/rise-phishing-detection/blob/main/scripts/processing/data_augmentation.py) the initial dataset (`emails.csv`) by adding additional columns. These columns are:

- `num_urls`: the number of URLs present
- `num_redirects`: the number of generic redirect links (i.e., bit.ly, tinyurl.com, etc.) present
- `num_words`: the number of words present in the email body
- `num_chars_foreign`: the number of characters not present in ASCII
- `num_chars_special`: the number of non-alphanumeric or space characters
- `num_urgent_words`: the number of words indicating urgency
- `num_stopwords`: the number of stopwords present
- `body_no_stopwords`: a copy of `body` with stopwords and special characters removed

The augmented data was exported as `emails_augmented.csv`.

## Methods

## Conclusions

## License

Please see our [LICENSE.md](LICENSE.md) file for more information.

## Acknowledgements

We would like to thank our mentors Patrick Bloniasz, Dr. Eugene Pinsky, Tharunya Katikireddy, Tejovan Parker, Zhengyang Shan, and Kevin Quinn for their support and contributions to our project. We would also like to extend our gratitude to Boston University and the Research in Science and Engineering program for this opportunity.
