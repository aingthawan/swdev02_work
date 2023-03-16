# a class for scraping the main page of the website
# then keep the raw content in the database with the url as key
# serving ELT process
#
# Dev : Aingkk.

import sqlite3


class rawKeeper:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.conn.cursor()
        self.createTable()

    # tested
    def createTable(self):
        """Create table for raw content"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS RawMaterial(URL, raw_content)")
        self.conn.commit()

    # tested
    def insertRaw(self, url, raw_content):
        """Insert the url and raw content into the table"""
        self.cursor.execute("INSERT INTO RawMaterial VALUES (?, ?)", (url, raw_content))
        self.conn.commit()
        
    # tested
    def removeRaw(self, url):
        """Remove the url from the table"""
        self.cursor.execute("DELETE FROM RawMaterial WHERE URL = ?", (url,))
        self.conn.commit()

    # tested
    def checkRaw(self, url):
        """Check if the url already exists in the table"""
        self.cursor.execute("SELECT URL FROM RawMaterial WHERE URL = ?", (url,))
        result = self.cursor.fetchone()
        return result

    def close(self):
        """Close the connection"""
        self.conn.commit()
        self.conn.close()