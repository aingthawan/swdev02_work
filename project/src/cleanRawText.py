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
import xml.etree.ElementTree as ET
    
class TextCleaners:
    """Designed for Inverted Indexing"""
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))

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

            # Only extract text from specific tags (e.g. p, h1, etc.)
            # for tag in ['p', 'h1', 'h2', 'h3', 'article']:
            for tag in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'article']:
                elements = root.findall(tag)
                for element in elements:
                    raw_text += element.text + " "

        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)