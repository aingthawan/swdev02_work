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
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.createTable()
    
    # tested
    def createTable(self):
        # Create table 
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Search_Cache (Query_List TEXT, ID_List TEXT)")
        self.conn.commit()
        
    def alreadyScrape(self, url_to_check):
        """Check whether url already scrape, Return in True or false"""
        # query_check = f"SELECT * FROM Web_Data WHERE URL='{url_to_check}'"
        self.cursor.execute("SELECT * FROM Web_Data WHERE URL=?", (url_to_check,))
        result = self.cursor.fetchone()

        if result is not None:
            return True
        else:
            return False

    
    # method for terminate the connection
    # def close(self):
    def __del__(self):
        """Close the connection"""
        self.conn.commit()
        self.conn.close