# File for LinkChecker 
# For checking URL accessibility, compare URL domain, check whether URL already scrape
# Dev : Aingkk

import sqlite3
from urllib.parse import urlparse

class LinkChecker:
    """Class for working on URLs"""
    
    def __init__(self, database_file):
        """Input Database file"""
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
    
    def alreadyScrape(self, url_to_check, table, column)
        """Check whether url already scrape, Return in True or false
        Table : Reference_Domain,   
        column_name : Domain_Name """

        query_check = f"SELECT * FROM {table_name} WHERE {column_name}='{url_to_check}'"
        self.cursor.execute(query_check)
        result = self.cursor.fetchone()

        if result:
            return True
        else:
            return False

    def checkAccessibility(self, url):
        """Check Whether URL is still accessible"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as err:
            return False

    def compareDomains(self, url1, url2):
        """Compare two url domain"""
        domain1 = urlparse(url1).hostname
        domain2 = urlparse(url2).hostname
        return domain1 == domain2
    
