# Class TextCleaner
# For Inverted Indexing
# Input : Raw Text   ------>>  Output : Cleaned Token
# To Use : obj.clean(raw_text)
#
# dev : Aingkk.
#                 UML Diagram
#                +---------------------+
#                |   TextCleaner       |
#                +---------------------+
#                | -nlp: spacy         |
#                | -stop_words         |
#                +---------------------+
#                | +__init__()         |
#                | +normalize()        |
#                | +remove_stopwords() |
#                | +lemmatize()        |
#                | +clean()            |
#                +---------------------+

import re
import spacy
from nltk.corpus import stopwords
from bs4 import BeautifulSoup

class TextCleaners:
    """Designed for Inverted Indexing"""
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))

    def normalize(self, raw_text):
        """Remove special characters and lowercase text"""
        return re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", raw_text.lower())

    def remove_emoji(self, text):
        """Remove emoji from text"""
        emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F" #emotions
                           u"\U0001F300-\U0001F5FF" #sumbols and pictographs
                           u"\U0001F680-\U0001F6FF" #transport and map symbols
                           u"\U0001F1E0-\U0001F1FF" #flags
                           u"\U00002702-\U000027B0"  
                           u"\U000024C2-\U0001F251" 

                           "]+",flags = re.UNICODE)
        return emoji_pattern.sub(r'', text)

    def remove_stopwords(self, raw_text):
        """Remove stopwords"""
        words = [word for word in raw_text.split() if word not in self.stop_words]
        return " ".join(words)

    def lemmatize(self, raw_text):
        """Perform lemmatization, return as a list of strings"""
        doc = self.nlp(raw_text)
        return [token.lemma_ for token in doc]

    def clean(self, raw_text):
        """Clean text by normalizing, removing stopwords, and lemmatizing"""
        # For user query
        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)   

    def clean_raw(self, raw_text):
        """Clean text by normalizing, removing stopwords, and lemmatizing"""
        # For raw text
        try: 
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(raw_text, 'html.parser')
            raw_text = ""

            # Only extract text from specific tags (e.g. p, h1, etc.)
            for tag in ['p', 'h1', 'h2', 'h3', 'article']:
                elements = soup.find_all(tag)
                for element in elements:
                    raw_text += " ".join(element.stripped_strings) + " "
        except:
            # If input is not HTML, try processing it as XML
            import xml.etree.ElementTree as ET
            root = ET.fromstring(raw_text)
            raw_text = ""

            # Only extract text from specific tags (e.g. p, h1, etc.)
            for tag in ['p', 'h1', 'h2', 'h3', 'article']:
                elements = root.findall(tag)
                for element in elements:
                    raw_text += element.text + " "

        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)

    
