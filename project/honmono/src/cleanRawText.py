# File for class TextCleaner
# For Inverted Indexing
# Input : Raw Text   ------>>  Output : Cleaned Token
# To Use : obj.clean(raw_text)
#
# dev : Aingkk.
#                 UML Diagram
#                +----------------+
#                |   TextCleaner  |
#                +----------------+
#                | -nlp: spacy    |
#                | -stop_words    |
#                +----------------+
#                | +__init__()    |
#                | +normalize()   |
#                | +remove_stopwords() |
#                | +lemmatize()   |
#                | +clean()       |
#                +----------------+

import re
import spacy
from nltk.corpus import stopwords

class TextCleaner:
    """Designed for Inverted Indexing"""
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.stop_words = set(stopwords.words('english'))

    def normalize(self, raw_text):
        """Remove special characters and lowercase text"""
        return re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^rt|http.+?", " ", raw_text.lower())

    def remove_stopwords(self, raw_text):
        """Remove stopwords"""
        words = [word for word in raw_text.split() if word not in self.stop_words]
        return " ".join(words)

    def lemmatize(self, raw_text):
        """Perform lemmatization"""
        doc = self.nlp(raw_text)
        return [token.lemma_ for token in doc]

    def clean(self, raw_text):
        """Clean text by normalizing, removing stopwords, and lemmatizing"""
        raw_text = self.normalize(raw_text)
        raw_text = self.remove_stopwords(raw_text)
        return self.lemmatize(raw_text)   

# Example
# obj = TextCleaner()
# print(obj.clean("Film Camera"))        