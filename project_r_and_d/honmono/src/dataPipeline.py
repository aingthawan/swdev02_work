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
   

    def uncountRef(domain_name_list, tableName, domainColumn, countColumn):
        """For uncount referenced domain"""
        for domain in domain_name_list:
            query_check = f"UPDATE {tableName} SET {countColumn} = {countColumn} - 1 WHERE {domainColumn} = '{domain}'"
            cursor.execute(query_check)
            conn.commit()

            
    def removeInvertedIndex(table_name, doc_freq_col, inverted_dict_col, words, web_id):
        """Remove id from indexing and reduce docsfreq"""

        for word in words:
            # Retrieve the current values of Document_Freq and Inverted_Dict
            self.cursor.execute(f"SELECT {doc_freq_col}, {inverted_dict_col} FROM {table_name} WHERE Word=?", (word,))
            result = self.cursor.fetchone()
            doc_freq, inverted_dict = result[0], result[1]

            # Decrement the Document_Freq value
            doc_freq -= 1

            # Convert the Inverted_Dict string to a dictionary and remove the entry for the Web_ID
            inverted_dict = eval(inverted_dict)
            inverted_dict.pop(str(web_id), None)

            # Update the values of Document_Freq and Inverted_Dict for the word
            self.cursor.execute(f"UPDATE {table_name} SET {doc_freq_col}=?, {inverted_dict_col}=? WHERE Word=?", (doc_freq, str(inverted_dict), word))

        # Commit the changes to the database
        self.conn.commit()
        
        
    def getUniqueID(self, table_name, web_id_column):
        """function for unique unused ID for a website"""
        self.cursor.execute(f"SELECT MAX({web_id_column}) FROM {table_name}")
        max_id = self.cursor.fetchone()[0]
        next_id = 1 if max_id is None else max_id + 1
        self.cursor.execute(f"SELECT {web_id_column} FROM {table_name} WHERE {web_id_column} = {next_id}")
        while self.cursor.fetchone() is not None:
            next_id += 1
        return next_id
    
    
    def updateReferenceDomain(self, table_name, domain_col, ref_col, domains):
        """Update reference domain receiving a list of domain"""
        for domain in domains:
            # Check if the domain already exists in the table
            self.cursor.execute(f"SELECT {ref_col} FROM {table_name} WHERE {domain_col}=?", (domain,))
            result = self.cursor.fetchone()
            
            if result:
                # If the domain already exists, increment the Ref_Count by 1
                ref_count = result[0] + 1
                self.cursor.execute(f"UPDATE {table_name} SET {ref_col}=? WHERE {domain_col}=?", (ref_count, domain))
            else:
                # If the domain doesn't exist, insert a new entry with Ref_Count set to 1
                self.cursor.execute(f"INSERT INTO {table_name} ({domain_col}, {ref_col}) VALUES (?, 1)", (domain,))
        
        # Commit the changes to the database
        self.conn.commit()
    
    
    def updateWebData(self, table_name, web_id_column, url_column, all_words_column, ref_to_column, url, web_id, words, domains):
        """Insert new url data into web_Data"""
        all_words = " ".join(words)
        ref_to = ",".join(domains)
        
        self.cursor.execute(f"INSERT INTO {table_name} ({web_id_column}, {url_column}, {all_words_column}, {ref_to_column}) VALUES (?, ?, ?, ?)", (web_id, url, all_words, ref_to))
        self.conn.commit()
        
        
    def updateInvertedIndexing(self, table_name, word_column, document_freq_column, inverted_dict_column, web_id, word_list):
        word_count = {}
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1
        for word, count in word_count.items():
            self.cursor.execute(f"SELECT {word_column} FROM {table_name} WHERE {word_column} = '{word}'")
            result = self.cursor.fetchone()
            if result:
                self.cursor.execute(f"UPDATE {table_name} SET {document_freq_column} = {document_freq_column} + 1, {inverted_dict_column} = {inverted_dict_column} || '{{{web_id}:{count}}}' WHERE {word_column} = '{word}'")
            else:
                self.cursor.execute(f"INSERT INTO {table_name} ({word_column}, {document_freq_column}, {inverted_dict_column}) VALUES ('{word}', 1, '{{{web_id}:{count}}}')")
        self.conn.commit()
        
    
    