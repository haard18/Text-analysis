import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import nltk
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
import os

# Read the Excel file
df = pd.read_excel('20211030 Test Assignment/Input.xlsx')

# Function to extract text from URLs
def url_text(url):
    try:
        paragraphs = []
        
        # Create a fake user agent
        user_agent = UserAgent().chrome
        
        # Make the request with the fake user agent
        data = requests.get(url, headers={"User-Agent": user_agent}).text
        
        soup = BeautifulSoup(data, 'lxml')
        
        # Extract title
        title = soup.find_all('h1')[0].text.strip() if soup.find_all('h1') else ''
        
        # Extract paragraphs
        p_tags = soup.find_all('p')
        
        for paragraph in p_tags:
            paragraph_text = paragraph.text.strip()
            if paragraph_text:  # Check if the paragraph is not empty
                paragraphs.append(paragraph_text)
        
        # Combine title and paragraphs
        text = ' '.join(paragraphs)
        text = title + " " + text
        
        return text
    except requests.HTTPError as e:
        print(f"HTTP Error {e.response.status_code}: {e.response.reason}")
        return None
    except Exception as e:
        print(f"Error extracting article from {url}: {e}")
        return None

# Apply the function to each row in the DataFrame
df['ARTICLE'] = df['URL'].apply(url_text)

# Define the directory containing the stop words files
directory = '20211030 Test Assignment/StopWords/'

# List all text files in the directory
file_list = [file for file in os.listdir(directory) if file.endswith('.txt')]

# Create a new combined stop words file
combined_file_path = 'combined_stopwords.txt'

with open(combined_file_path, 'w') as combined_file:
    for file_name in file_list:
        file_path = os.path.join(directory, file_name)
        
        # Read the content of each file and append to the combined file
        with open(file_path, 'r') as file:
            content = file.read()
            combined_file.write(content)
            combined_file.write('\n')  # Add a new line between each file's content

print(f"Combined stop words saved to '{combined_file_path}'.")

# Download necessary nltk resources
nltk.download('punkt')
nltk.download('stopwords')

# Load combined stopwords
with open('combined_stopwords.txt', 'r') as file:
    stop_words = set(file.read().splitlines())

# Load positive and negative word lists
positive_words = set()
negative_words = set()

# Load positive words
with open('20211030 Test Assignment/MasterDictionary/positive-words.txt', 'r') as file:
    for line in file:
        word = line.strip()
        if word not in stop_words:
            positive_words.add(word)

# Load negative words
with open('20211030 Test Assignment/MasterDictionary/negative-words.txt', 'r') as file:
    for line in file:
        word = line.strip()
        if word not in stop_words:
            negative_words.add(word)
# Function to clean the text
def clean_text(text):
    # Retain punctuation marks
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    # Join tokens to form cleaned text
    cleaned_text = ' '.join(cleaned_tokens)
    
    return cleaned_text
# Function to calculate the scores
def calculate_scores(text):
    tokens = word_tokenize(text.lower())
    cleaned_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    positive_score = sum(1 for word in cleaned_tokens if word in positive_words)
    negative_score = sum(1 for word in cleaned_tokens if word in negative_words)
    
    polarity_score = (positive_score - negative_score) / ((positive_score + negative_score) + 0.000001)
    subjectivity_score = (positive_score + negative_score) / (len(cleaned_tokens) + 0.000001)
    
    return positive_score, negative_score, polarity_score, subjectivity_score
# Function to calculate the Fog Index
def calculate_fog_index(avg_sentence_length, percentage_complex_words):
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)
    return fog_index

def calculate_readability(text):
    sentences = sent_tokenize(text)
    words = word_tokenize(text.lower())
    
    # Check if there are any sentences or words to avoid ZeroDivisionError
    if len(sentences) == 0 or len(words) == 0:
        avg_sentence_length = 0
        percentage_complex_words = 0
        avg_words_per_sentence = 0
        total_words = 0
        syllable_count_per_word = 0
        avg_word_length = 0
        complex_word_count = 0
        fog_index = 0 
    else:
        avg_sentence_length = len(words) / len(sentences)
        
        # Percentage of Complex words
        complex_words = [word for word in words if syllable_count(word) > 2]
        percentage_complex_words = (len(complex_words) / len(words)) * 100
        
        # Average Number of Words Per Sentence
        avg_words_per_sentence = len(words) / len(sentences)
        
        # Complex Word Count
        complex_word_count = len(complex_words)
        
        # Word Count
        total_words = len(words)
        
        # Syllable Count Per Word
        syllable_count_per_word = sum(syllable_count(word) for word in words) / total_words
        fog_index = calculate_fog_index(avg_sentence_length, percentage_complex_words)
        
        # Average Word Length
        avg_word_length = sum(len(word) for word in words) / total_words
    
    # Personal Pronouns
    personal_pronouns = len(re.findall(r'\b(?:i|we|my|ours|us)\b', text.lower()))
    
    return avg_sentence_length, percentage_complex_words, fog_index, avg_words_per_sentence, complex_word_count, total_words, syllable_count_per_word, personal_pronouns, avg_word_length

def syllable_count(word):
    vowels = 'aeiouy'
    count = 0
    word = word.lower()
    
    # Handle exceptions like words ending with "es", "ed"
    if word.endswith(('es', 'ed')):
        pass
    elif word[0] in vowels:
        count += 1
    
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    
    if count == 0:
        count += 1
    
    return count

# Clean the text
df['CLEANED ARTICLE'] = df['ARTICLE'].apply(clean_text)

df['POSITIVE SCORE'], df['NEGATIVE SCORE'], df['POLARITY SCORE'], df['SUBJECTIVITY SCORE'] = zip(*df['CLEANED ARTICLE'].apply(calculate_scores))

# Calculate readability metrics
(df['AVERAGE SENTENCE LENGTH'], df['PERCENTAGE OF COMPLEX WORDS'], df['AVG WORDS PER SENTENCE'],
 df['COMPLEX WORD COUNT'], df['FOG INDEX'], df['WORD COUNT'], df['SYLLABLE COUNT PER WORD'],
 df['PERSONAL PRONOUNS'], df['AVG WORD LENGTH']) = zip(*df['ARTICLE'].apply(calculate_readability))

# Save the updated DataFrame to a new CSV file
df.to_csv('analysis_results.csv', index=False)

print("Text analysis completed and saved to 'analysis_results.csv'.")

# Read the CSV file
df = pd.read_csv('analysis_results.csv')

# Selecting the desired columns in the specified order
selected_columns = [
    'URL_ID', 'URL', 'POSITIVE SCORE', 'NEGATIVE SCORE', 'POLARITY SCORE','SUBJECTIVITY SCORE',
    'AVERAGE SENTENCE LENGTH', 'PERCENTAGE OF COMPLEX WORDS', 'FOG INDEX',
    'AVG WORDS PER SENTENCE', 'COMPLEX WORD COUNT', 'WORD COUNT',
    'SYLLABLE COUNT PER WORD', 'PERSONAL PRONOUNS', 'AVG WORD LENGTH'
]

df_selected = df[selected_columns]

# Write the selected columns to an Excel file
df_selected.to_excel('Results.xlsx', index=False)

print("CSV file converted to Excel format successfully!")
