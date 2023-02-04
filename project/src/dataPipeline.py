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

class dataPipeline:
    """Class of function for Update / Remove data"""
    
    def __init__(self, database_file):
        """Input database file"""
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.createTable()
        
    def createTable(self):
        # Create table for keeping domain name of url and times of referenced to
        cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        # Create a table for unique id for each url and list of all words in that url and list of url found on that page
        cursor.execute("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To)")
        # Create table for each word, number of documnet that conatain that word and dictionary of sorted key that are id of url and number of that word found on that link
        cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")

    def uncountRef(self, domain_name_list):
        """For uncount referenced domain"""
        for domain in domain_name_list:
            query_check = f"UPDATE Reference_Domain SET Ref_Count = Ref_Count - 1 WHERE Domain_Name = '{domain}'"
            cursor.execute(query_check)
            conn.commit()

            
    def removeInvertedIndex(self, words, web_id):
        """Remove id from indexing and reduce docsfreq"""

        for word in words:
            # Retrieve the current values of Document_Freq and Inverted_Dict
            self.cursor.execute(f"SELECT Document_Freq, Inverted_Dict FROM Inverted_Index WHERE Word=?", (word,))
            result = self.cursor.fetchone()
            doc_freq, inverted_dict = result[0], result[1]

            # Decrement the Document_Freq value
            doc_freq -= 1

            # Convert the Inverted_Dict string to a dictionary and remove the entry for the Web_ID
            inverted_dict = eval(inverted_dict)
            inverted_dict.pop(str(web_id), None)

            # Update the values of Document_Freq and Inverted_Dict for the word
            self.cursor.execute(f"UPDATE Inverted_Index SET Document_Freq=?, Inverted_Dict=? WHERE Word=?", (doc_freq, str(inverted_dict), word))

        # Commit the changes to the database
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
    

    # ==============================================================

    
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
    
    def updateWebData(self, web_id, url, all_words, ref_to):
        """Insert new url data into web_Data"""
        all_words = " ".join(words)
        ref_to = ",".join(domains)
        
        self.cursor.execute(f"INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, ?, ?, ?)", (web_id, url, all_words, ref_to))
        self.conn.commit()
        
    
    # cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")
    def updateInvertedIndexing(self, web_id, word_list):
        word_count = {}
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1
        for word, count in word_count.items():
            self.cursor.execute(f"SELECT Word FROM Inverted_Index WHERE Word = '{word}'")
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute(f"UPDATE Inverted_Index SET Document_Freq = Document_Freq + 1, Inverted_Dict = Inverted_Dict || '{{{web_id}:{count}}}' WHERE Word = '{word}'")
            else:
                self.cursor.execute(f"INSERT INTO Inverted_Index (Word, Document_Freq, Inverted_Dict) VALUES ('{word}', 1, '{{{web_id}:{count}}}')")
        self.conn.commit()
        