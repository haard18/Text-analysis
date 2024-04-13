# Web Article Text Analysis

This project aims to automate the extraction of textual content from web articles, conduct sentiment analysis, and compute readability metrics. The resultant data is organized and saved in an Excel format for easy analysis and reporting.

## Approach HighLevel

To achieve the project's goals, a structured approach was implemented, subdividing the main task into focused sub-tasks for a systematic and efficient workflow:

1. **Data Scraping**: Fetching web articles from provided URLs.
2. **Text Cleaning and Preprocessing**: Refining the extracted text to remove noise and irrelevant content.
3. **Original Data Preservation**: Maintaining an untouched copy of the fetched articles.
4. **Variable Identification**: Calculating various metrics related to sentiment and readability.
5. **Result Compilation**: Aggregating the processed data into a structured Excel file.

### Below You can read through the detailed Methodology concerning each Step

## Methodology

### Data Retrieval

1. **URL Dataset Integration**: The project initiates by reading an Excel file containing URLs into a pandas DataFrame.
2. **Web Content Extraction**: Leveraging the `requests` and `BeautifulSoup` libraries, a function (`url_text`) is devised to fetch the textual content from each URL.

### Text Preprocessing

1. **Stopword Compilation**: A comprehensive list of stopwords is curated by amalgamating data from multiple source files.
2. **Text Sanitization**: The extracted text undergoes rigorous cleaning to eliminate stopwords, punctuation marks, and non-alphabetic characters through tokenization and selective filtering.

### Sentiment Evaluation

1. **Sentiment Lexicon Initialization**: Datasets containing positive and negative words are loaded from external files.
2. **Score Derivation**: The sentiment scores, namely positive, negative, polarity, and subjectivity, are computed based on the refined text and the aforementioned lexicons.

### Readability Analysis

1. **Sentence Structure Analysis**: The average sentence length is deduced by dividing the total word count by the number of sentences.
2. **Complexity Assessment**: Words with more than two syllables are classified as complex words.
3. **Fog Index Calculation**: Utilizing the formula: `0.4 * (average sentence length + percentage of complex words)`.
4. **Personal Pronoun Count**: The occurrence count of personal pronouns (e.g., I, we, my, ours, us) in the text is determined.

### Result Compilation

1. **Data Aggregation**: The computed metrics are integrated into the original DataFrame.
2. **Column Selection**: A subset of columns is chosen, ordered as per specified requirements.
3. **Excel Export**: The resultant DataFrame is exported as an Excel workbook named Result.xlsx

## Prerequisites

Prior to executing the script, ensure the following Python libraries are installed:

- `pandas`
- `requests`
- `BeautifulSoup4`
- `fake_useragent`
- `nltk`

To install the dependencies, execute the following command:

```bash
pip install pandas requests beautifulsoup4 fake_useragent nltk
```

Moreover, download the `punkt` and `stopwords` datasets using the NLTK package:

```bash
import nltk
nltk.download('punkt')
nltk.download('stopwords')
```

## Execution(Running the Code)

1. Download the Google Drive Folder
2. Setup a **Python** Environment and Install all Dependencies
3. A reference To Needed Packages can be found in **requirements.txt**
4. Run ``python3 work.py``
5. Analyze the Generated ``Hello.xlsx``.
