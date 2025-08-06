# PhishFence: Phishing Detection with Explainable AI

[![lifecycle](https://img.shields.io/badge/lifecycle-experimental-orange)](https://lifecycle.r-lib.org/articles/stages.html)
[![license](https://img.shields.io/badge/license-MIT_/_CC_BY--SA_4.0-blue)](LICENSE.md)

## Abstract

Phishing attacks remain a prevalent and financially damaging threat in digital communications, affecting both vulnerable individuals and large companies. Attacks are increasingly leveraging obfuscation techniques to deceive end-users and evade traditional spam filters. Furthermore, conventional “black box” phishing detection techniques fail to provide clear explanations to end-users regarding classification decisions, resulting in poor transparency and trust.

We propose **PhishFence**, a phishing email detection pipeline that utilizes a BERT-based tokenization and classification approach to achieve high detection accuracy. To address the lack of transparency in traditional classifiers, we integrate SHAP (SHapley Additive exPlanations) to generate feature-level explanations. These SHAP outputs are interpreted by the OpenAI API into natural language, making classification rationale understandable to end-users. Our unified dataset, comprising six publicly available datasets, contains approximately 82,000 emails that represent a diverse range of phishing tactics. In addition to a BERT-based approach, we evaluate the accuracy, precision, recall, and F1-score of two vectorization techniques—TF-IDF and Sentence-BERT—combined with four classifiers: logistic regression, random forest, naive Bayes, and multi-layer perceptron.

The BERT-based model achieves 99.3% accuracy, outperforming the other four models across all key metrics. Additionally, we develop a web application that enables users to submit emails for quick and reliable classification. Overall, PhishFence matches the performance of leading phishing detection models while providing approachable feature-level explanations for decisions, demonstrating the effectiveness of pairing explainable AI with classification models in phishing detection.

## Repository Structure

```
phishfence
├─ (.env)
├─ .gitattributes
├─ .gitignore
├─ LICENSE.md
├─ README.md
├─ environment.yml
├─ data/
│  ├─ analysis/
│  │  ├─ APPENDIX.md
│  │  └─ ...
│  └─ input/
│     ├─ SOURCES.md
│     └─ ...
├─ output/
│  ├─ appendix/...
│  ├─ embeddings/...
│  ├─ models/
│  │  ├─ phishing-bert-model/...
│  │  └─ ...
│  └─ results/...
├─ scripts/
│  ├─ analysis/...
│  ├─ appendix/...
│  ├─ processing/...
│  ├─ new.ipynb
│  └─ main.py
└─ web/
   ├─ static/style.css
   ├─ templates/index.html
   ├─ requirements.txt
   └─ app.py
```

## Data

We used a variety of publicly available datasets. The raw data is contained within `phishfence/data/input`. The sources for the data are noted in [`phishfence/data/input/metadata/SOURCES.md`](https://github.com/thomasha1310/phishfence/blob/main/data/input/metadata/SOURCES.md).

### Pre-Processing

Since each dataset had different columns, we trimmed each dataset to include only the `subject`, `body`, and `label` columns. The six trimmed datasets were then concatenated to create a complete dataset.

All duplicate rows and rows with missing values were removed, and the dataset was exported as `emails.csv`. This processed dataset contains 82,138 entries, of which 39,527 (48%) are legitimate and 42,611 (52%) are malicious.

### Handling the Enron Corpus

After initial testing, we determined that the Enron corpus (29,767 emails) comprised an overly large proportion (roughly 36%) of the total dataset. In particular, when using LIME to explain model behaviors, the word "Enron" consistently appeared as the top indicative word for legitimate emails, with a score of -11.0770.

To prevent overfitting to the Enron corpus, we replaced all instances of the word "Enron" in the `Enron.csv` with a randomly selected company from the Fortune 500 list of companies before recompiling the full dataset.

### Data Augmentation

To increase the training options available to us, we [augmented](https://github.com/thomasha1310/phishfence/blob/main/scripts/processing/augmentation.py) the initial dataset (`emails.csv`) by adding additional columns. These columns are:

- `num_urls`: the number of URLs present
- `num_words`: the number of words present in the email body
- `num_chars_foreign`: the number of characters not present in ASCII
- `num_chars_special`: the number of non-alphanumeric or space characters
- `num_urgent_words`: the number of words indicating urgency
- `num_stopwords`: the number of stopwords present
- `body_no_stopwords`: a copy of `body` with stopwords and special characters removed

The augmented data was exported as `emails_augmented.csv`.

## Installation & Usage

Clone the repository:
```
git clone https://github.com/thomasha1310/phishfence.git
cd phishfence
```

### Web Application

Install dependencies with pip:
```
pip install -r web/requirements.txt
```

Create a `.env` file in `phishfence/` with your Gemini API key:
```
GEMINI_API_KEY="<YOUR API KEY HERE>"
```

Activate the Flask server:
```
python web/app.py
```

## License

Please visit our [license](https://github.com/thomasha1310/phishfence/blob/main/LICENSE.md) file for more information.

## Acknowledgements

We would like to thank our mentors, [Patrick Bloniasz](https://github.com/bloniaszp), [Dr. Eugene Pinsky](https://www.bu.edu/met/profile/eugene-pinsky/), Tharunya Katikireddy, [Tejovan Parker](https://www.tejovanparker.com/), [Zhengyang Shan](https://github.com/ZhengyangShan), and [Kevin Quinn](https://github.com/kevinqnb), for their support and contributions to our project. We would also like to extend our gratitude to [Boston University](https://www.bu.edu/) and the [BU RISE](https://www.bu.edu/summer/high-school-programs/rise-internship-practicum/) program for this opportunity.
