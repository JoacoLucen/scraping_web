import requests
from bs4 import BeautifulSoup
from data_base import save_titles

def get_html(url):
    """Fetch the HTML content of a given URL.
    Args:
        url (str): The URL to fetch.
    Returns:
        str: The HTML content of the page or None if the request fails."""
    
    try:
        # User-Agent header to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        response = requests.get(url, headers=headers, timeout=10)

        # Verify if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to retrieve the page: Status code {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching the page: {e}")
        return None


# Extracting news titles from TN (Todo Noticias), C5N (Canal 5 Noticias), LN (La Nación), and Clarin
def extract_news_titles(html):
    """Extract news titles from the HTML content.
    Args:
        html (str): The HTML content of the page.
    Returns:
        list: A list of news titles."""
    
    soup = BeautifulSoup(html, 'html.parser')
    titles = []
    
    # Assuming news titles are within <h2> tags with a specific class
    for title in soup.find_all(['h1','h2','h3']):
       if title.text.strip() and len(title.text.strip()) > 15:
           titles.append(title.text.strip())
    
    for element in soup.select('card_headline'):
        if element.text.strip() and element.text.strip() not in titles:
            titles.append(element.text.strip())
    
    return titles

links = {
    'TN': 'https://tn.com.ar/',
    'C5N': 'https://www.c5n.com/',
    'LN': 'https://www.lanacion.com.ar/', 
    'Clarin': 'https://www.clarin.com/'
}

for key, url in links.items():
    html = get_html(url)
    if html:
        titles = extract_news_titles(html)
        if titles:
            print(f"The scraping of page {key} was successful")
            print(f"Number of titles found: {len(titles)}")
            save_titles(key, titles)
        else:
            print(f"No titles found on page {key}")
