# File for class data_manage
# For Inverted Indexing
#
# dev : Aingkk.
#                        UML DIAGRAM
#                        +-----------------+
#                        |  data_manage    |
#                        +-----------------+
#                        | -conn: sqlite3.connect 
#                        | -cursor: sqlite3.Cursor
#                        +-----------------+
#                        | +__init__(db_file:str)
#                        | +connect_db(db_file:str)
#                        | +create_table()
#                        | +insert_webData(web_url:str)
#                        | +insert_domainRef(domain:str, ref_count:int)
#                        | +insert_invertedIndex(gram:str, docs_freq:str, id_dict:dict)
#                        | +remove_webData(web_id:int)
#                        | +remove_domainRef(domain:str)
#                        | +remove_invertedIndex(gram:str)
#                        | +__del__()
#                        +-----------------+



import sqlite3
import json

class data_manage():
    def __init__(self, db_file):
        self.connect_db(db_file)
        self.create_table()
        
    def connect_db(self, db_file):
        """Connect to database"""
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
    
    def create_table(self):
        """Create table if doesn't exists (webData, domainRef, invertedIndex)"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS webData (web_id INT, web_url TEXT)")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS domainRef (domain TEXT, ref_count INT)")
        self.conn.commit()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS invertedIndex (gram TEXT, docs_freq TEXT, id_dict TEXT)")
        self.conn.commit()
        
    def insert_webData(self, web_url):
        """Insert data into webData table, generate unique web_id"""
        self.cursor.execute("SELECT MAX(web_id) FROM webData")
        max_id = self.cursor.fetchone()[0]
        if max_id is None:
            web_id = 1
        else:
            web_id = max_id + 1
            
        self.cursor.execute("INSERT INTO webData VALUES (?,?)", (web_id, web_url))
        self.conn.commit()
        
    def insert_domainRef(self, domain, ref_count):
        """Insert data into domainRef table"""
        self.cursor.execute("INSERT INTO domainRef VALUES (?,?)", (domain, ref_count))
        self.conn.commit()

    def insert_invertedIndex(self, gram, docs_freq, id_dict):
        """Insert data into invertedIndex table, support input id_dict as python dictionary"""
        id_dict = json.dumps(id_dict)
        self.cursor.execute("INSERT INTO invertedIndex VALUES (?,?,?)", (gram, docs_freq, id_dict))
        self.conn.commit()
        
    def remove_webData(self, web_id):
        """Remove data from webData table by web_id"""
        self.cursor.execute("DELETE FROM webData WHERE web_id = ?", (web_id,))
        self.conn.commit()
        
    def remove_domainRef(self, domain):
        """Remove data from domainRef table by domain"""
        self.cursor.execute("DELETE FROM domainRef WHERE domain = ?", (domain,))
        self.conn.commit()
        
    def remove_invertedIndex(self, gram):
        """Remove data from invertedIndex table by gram"""
        self.cursor.execute("DELETE FROM invertedIndex WHERE gram = ?", (gram,))
        self.conn.commit()
    
    def __del__(self):
        """close connection"""
        self.conn.close()
        


