import sqlite3

class raw_manager:
    """Class for working on raw database,
    Consists of methods for creating table, 
    inserting new raw content, 
    checking if url already exists in the table, 
    removing row from the table and closing the connection
    """
    
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def __del__(self):
        """Close the connection"""
        self.conn.commit()
        self.conn.close()
        
    def create_table(self):
        """Create table for raw content"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS raw_data(URL, raw_content)")
        self.conn.commit()
    
    def url_exist_check(self, url):
        """Check if url already exists in the table of raw database, return True or False"""
        self.cursor.execute("SELECT URL FROM raw_data WHERE URL = ?", (url,))
        if self.cursor.fetchone() is not None:
            return True
        else:
            return False
        
    def insert_new(self, url, raw_content):
        """Insert new raw content into the database"""
        self.cursor.execute("INSERT INTO raw_data VALUES (?, ?)", (url, raw_content))
        self.conn.commit()
        # print("raw_manager : New raw content inserted into the table")
        
    def remove(self, url):
        """Remove row related to the url from the table"""
        # try to remove the row
        try:
            self.cursor.execute("DELETE FROM raw_data WHERE URL = ?", (url,))
            self.conn.commit()
            # print log message
            print("raw_manager : URL removed from the table")
        # if the url is not in the table, print error message
        except sqlite3.OperationalError:
            print("raw_manager : URL not found in the table")
            pass

    def fetch_raw(self, url):
        """Fetch a raw content from the database, 
        return raw content (url , raw_content)
        if nothing left, return None
        """
