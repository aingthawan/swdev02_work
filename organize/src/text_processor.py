import re
import spacy
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import requests
from urllib.parse import urlparse
    
class text_processor:
    """Designed for Inverted Indexing"""
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def url_accessibility_check(self, url):
        """Check if url is accessible, return True or False"""
        if requests.head(url, headers=self.headers).status_code == 200:
            return True
        else:
            return False

    # tested
    def normalize(self, raw_text):
        """Remove special characters and lowercase text"""
        return re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", raw_text.lower())

    # tested
    def remove_stopwords(self, raw_text):
        """Remove stopwords"""
        words = [word for word in raw_text.split() if word not in self.stop_words]
        return " ".join(words)

    # tested
    def lemmatize(self, raw_text):
        """Perform lemmatization, return as a list of strings"""
        doc = self.nlp(raw_text)
        return [token.lemma_ for token in doc]

    # tested
    def clean(self, raw_text):
        """Clean text by normalizing, removing stopwords, and lemmatizing"""
        # For user query
        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)   

    # tested
    def clean_raw(self, raw_text):
        """Clean text by normalizing, removing stopwords, and lemmatizing"""
        # For raw text
        try: 
            soup = BeautifulSoup(raw_text, 'html.parser')
            raw_text = ""

            # Only extract text from specific tags (e.g. p, h1, etc.)
            for tag in ['p', 'h1', 'h2', 'h3', 'article']:
                elements = soup.find_all(tag)
                for element in elements:
                    raw_text += " ".join(element.stripped_strings) + " "
        except:
            # If input is not HTML, try processing it as XML
            root = ET.fromstring(raw_text)
            raw_text = ""

            for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article']:
                elements = root.findall(tag)
                for element in elements:
                    raw_text += element.text + " "

        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)

    def get_raw_html(self, url):
        """get raw html soup obj using a rotating proxy"""
        return requests.get(url, headers=self.headers).text

    def scrape_raw_text(self, html_text):
        """Return raw text string from bs4 object"""
        soup = BeautifulSoup(html_text, 'html.parser')
        text_content = soup.get_text()        
        text_content = text_content.strip()
        return text_content

    def scrape_all_urls(self, html_text):
        """Get all urls from a page, return a list of a unique urls"""
        soup = BeautifulSoup(html_text, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            url = link['href']
            if re.match(r'^https?://', url) and not re.search(r'\.(jpg|jpeg|png|gif)$', url):
                urls.add(url)
        return list(urls)

    def scrape_page(self, url):
        """Return a dictionary of url, all unrepeated backlinks and raw text"""
        raw_soup_html = self.get_raw_html(url).text
        # if not none
        if raw_soup_html is not None:
            return {
                "url" : url,
                "backlinks" : self.scrape_all_urls(raw_soup_html),
                "rawText" : self.scrape_raw_text(raw_soup_html)
            }
        else:
            return None