# File for LinkChecker 
# For checking URL accessibility, compare URL domain, check whether URL already scrape
# Dev : Aingkk

import sqlite3
from urllib.parse import urlparse
import requests
 
class LinkCheckers:
    """Class for working on URLs"""
    
    def __init__(self, database_file):
        """Input Database file"""
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.conn.cursor()

        self.createTable()
    
    # tested
    def createTable(self):
        # Create table for keeping domain name of url and times of referenced to
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        # Create a table for unique id for each url and list of all words in that url and list of url found on that page
        self.cursor.execute("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To)")
        # Create table for each word, number of document that contain that word and dictionary of sorted key that are id of url and number of that word found on that link
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Search_Cache (Query_List TEXT, ID_List TEXT)""")
        
    def alreadyScrape(self, url_to_check):
        """Check whether url already scrape, Return in True or false"""

        # query_check = f"SELECT * FROM Web_Data WHERE URL='{url_to_check}'"
        self.cursor.execute(f"SELECT * FROM Web_Data WHERE URL='{url_to_check}'")
        result = self.cursor.fetchone()

        if result != None:
            return True
        else:
            return False

    # def checkAccessibility(self, url):
    #     """Check Whether URL is still accessible"""
    #     try:
    #         response = requests.get(url)
    #         response.raise_for_status()
    #         return True
    #     except requests.exceptions.HTTPError as err:
    #         return False

    def checkAccessibility(self, url):
        """Check Whether URL is still accessible"""
        try:
            response = requests.get(url)
            response.raise_for_status()
            return True
        except (requests.exceptions.HTTPError, requests.exceptions.RequestException) as err:
            return False

    # tested
    def get_domain(self, url):
        """Get domain name from url"""
        if len(url) > 0 and (url != None):
            Domain_name = ""
            x = url.split("/")
            if(x[0] == "https:" or x[0] == "http:"):
                x = x[2].split(".")
            else:
                x = x[0].split(".")
            if(len(x) == 2):
                Domain_name = x[0]
            else:
                Domain_name = x[1] 

            return Domain_name
        else:
            return ""
        

    # def compareDomains(self, url1, url2):
    #     """Compare two url domain"""
    #     # get domain name from url, don't include subdomain
    #     domain1 = urlparse(url1).netloc.split('.')[-2:]
    #     domain2 = urlparse(url2).netloc.split('.')[-2:]
    #     return domain1 == domain2

    # tested
    def compareDomains(self, url1, url2):
        """Compare two url domain"""
        return self.get_domain(url1) == self.get_domain(url2)
    
    # method for terminate the connection
    def close(self):
        """Close the connection"""
        # commit the changes
        self.conn.commit()
        self.conn.close