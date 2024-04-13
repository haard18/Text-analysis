import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

# Read the Excel file
df = pd.read_excel('20211030 Test Assignment/Input.xlsx')

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

# Save the updated DataFrame to a new Excel file
df.to_excel('output.xlsx', index=False)

print("Extraction completed and saved to 'output.xlsx'.")
