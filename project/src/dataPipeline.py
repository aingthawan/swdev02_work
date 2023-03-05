# A file for class dataPipeline
# This class is for update / remove data from database
# Dev : Aingkk.
# 
# uncountRef: decrement the reference count of a domain in a database table.
# removeInvertedIndex: remove the id of a website from an inverted index table.
# getUniqueID: get the next unused id for a website in a table.
# updateReferenceDomain: update the reference domain in a table by either incrementing the count or inserting a new domain.
# updateWebData: insert new data for a website into the table for web data.
# updateInvertedIndexing: update the inverted index table with the word count for each word in the website data.

import sqlite3
import ast

class dataPipelines:
    """Class of function for Update / Remove data"""
    
    def __init__(self, database_file):
        """Input database file"""
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.createTable()
        
    def createTable(self):
        # Create table for keeping domain name of url and times of referenced to
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        # Create a table for unique id for each url and list of all words in that url and list of url found on that page
        self.cursor.execute("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To)")
        # Create table for each word, number of document that contain that word and dictionary of sorted key that are id of url and number of that word found on that link
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")

    def uncountRef(self, domain_name_list):
        """For uncount referenced domain"""
        for domain in domain_name_list:
            # query_check = f"UPDATE Reference_Domain SET Ref_Count = Ref_Count - 1 WHERE Domain_Name = '{domain}'"
            self.cursor.execute(f"UPDATE Reference_Domain SET Ref_Count = Ref_Count - 1 WHERE Domain_Name = '{domain}'")
            self.conn.commit()
    
    def removeInvertedIndex(self, web_id, words):
        """Remove id from indexing and reduce docsfreq"""
        for word in words:
            self.cursor.execute("SELECT Inverted_Dict FROM Inverted_Index WHERE Word=?", (word,))
            inverted_dict = eval(self.cursor.fetchone()[0])
            inverted_dict.pop(web_id, None)
            self.cursor.execute(f"UPDATE Inverted_Index SET Document_Freq=Document_Freq-1, Inverted_Dict=? WHERE Word=?", (str(inverted_dict), word))
        self.conn.commit()

        
    def removeWebData(self, url):
        """Remove data from web_Data"""
        self.cursor.execute(f"DELETE FROM web_Data WHERE URL=?", (url,))
        self.conn.commit()

    # ==============================================================

    def getUniqueID(self):
        """function for unique unused ID for a website"""
        self.cursor.execute(f"SELECT MAX(Web_ID) FROM web_Data")
        max_id = self.cursor.fetchone()[0]
        next_id = 1 if max_id is None else max_id + 1
        self.cursor.execute(f"SELECT Web_ID FROM web_Data WHERE Web_ID = {next_id}")
        while self.cursor.fetchone() is not None:
            next_id += 1
        return next_id
    
    def fetch_data_by_url(self, url):
        """get data from row by url"""
        self.cursor.execute("SELECT Web_ID, URL, All_Word, Ref_To FROM web_Data WHERE URL=?", (url,))
        # Fetch the result
        result = self.cursor.fetchone()
        # if found, then return the result
        if result:
            # Return the result
            return {
                'Web_ID' : result[0],
                'URL' : result[1],
                'All_Word' : result[2].split(' , '),
                'Ref_To' : result[3].split(' , ')
            }
        # if not found, return None
        else:
            return None

    def fetch_data_by_id(self, web_id):
        """get data from row by id"""
        self.cursor.execute("SELECT Web_ID, URL, All_Word, Ref_To FROM web_Data WHERE Web_ID=?", (web_id,))
        # Fetch the result
        result = self.cursor.fetchone()
        # if found, then return the result
        if result:
            # Return the result
            return {
                'Web_ID' : result[0],
                'URL' : result[1],
                'All_Word' : result[2].split(' , '),
                'Ref_To' : result[3].split(' , ')
            }
        # if not found, return None
        else:
            return None


    # cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
    def updateReferenceDomain(self, domains):
        """Update reference domain receiving a list of domain"""
        for domain in domains:
            # Check if the domain already exists in the table
            self.cursor.execute(f"SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name=?", (domain,))
            result = self.cursor.fetchone()
            
            if result:
                # If the domain already exists, increment the Ref_Count by 1
                ref_count = result[0] + 1
                self.cursor.execute(f"UPDATE Reference_Domain SET Ref_Count=? WHERE Domain_Name=?", (ref_count, domain))
            else:
                # If the domain doesn't exist, insert a new entry with Ref_Count set to 1
                self.cursor.execute(f"INSERT INTO Reference_Domain (Domain_Name, Ref_Count) VALUES (?, 1)", (domain,))
        
        # Commit the changes to the database
        self.conn.commit()
    
#     OKAY ================================================================================
    def updateWebData(self, web_id, url, all_words, ref_to):
        """Insert new url data into web_Data"""
        words = list(all_words.keys())
        all_words = " , ".join(words)
        ref_to = " , ".join(ref_to)
        
        self.cursor.execute(f"INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, ?, ?, ?)", (web_id, url, all_words, ref_to))
        self.conn.commit()
        
    
    # cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")
    def updateInvertedIndexing(self, web_id, word_list):
        word_count = {}
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1
        for word, count in word_count.items():
            self.cursor.execute(f"SELECT Word, Inverted_Dict FROM Inverted_Index WHERE Word = '{word}'")
            result = self.cursor.fetchone()
            if result:
                inverted_dict = eval(result[1])
                inverted_dict[web_id] = count
                inverted_dict = str(inverted_dict)
                self.cursor.execute(f"UPDATE Inverted_Index SET Document_Freq = Document_Freq + 1, Inverted_Dict = '{inverted_dict}' WHERE Word = '{word}'")
            else:
                self.cursor.execute(f"INSERT INTO Inverted_Index (Word, Document_Freq, Inverted_Dict) VALUES ('{word}', 1, '{{{web_id}:{count}}}')")
            # sort column by Word
            # self.cursor.execute("SELECT * FROM Inverted_Index ORDER BY Word ASC")
            # self.conn.commit()
        self.conn.commit()
        
    # method for terminate the connection
    def close(self):
        """Close the connection"""
        # commit the changes
        self.conn.commit()
        self.conn.close

    