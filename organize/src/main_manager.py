import sqlite3

class main_manager:
    """Class for working on main database,"""
    
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.cursor = self.conn.cursor()
        self.create_table()
        
    def __del__(self):
        """Close the connection"""
        self.conn.commit()
        self.conn.close()
        
    def create_table(self):
        """Create table for main content"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS reference_domain(domain_name, ref_count)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS web_data(web_id, url, all_word, ref_to)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS inverted_index(word, document_freq, inverted_dict)")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS search_cache(query_list, ID_List)")
        self.conn.commit()
        
    def url_exist_check(self, url):
        """Check if url already exists in the table web_data of main database, return True or False"""
        if self.cursor.execute("SELECT url FROM web_data WHERE url = ?", (url,)).fetchone() is not None:
            return True
        else:
            return False
    
    def domain_exist_check(self, domain):
        """Check if domain already exists in the table reference_domain of main database, return True or False"""
        if self.cursor.execute("SELECT domain_name FROM reference_domain WHERE domain_name = ?", (domain,)).fetchone() is not None:
            return True
        else:
            return False
        
    def word_exist_check(self, word):
        """Check if word already exists in the table inverted_index of main database, return True or False"""
        if self.cursor.execute("SELECT word FROM inverted_index WHERE word = ?", (word,)).fetchone() is not None:
            return True
        else:
            return False
        
    def id_exist_check(self, ID):
        """Check if ID already exists in the table web_data of main database, return True or False"""
        if self.cursor.execute("SELECT web_id FROM web_data WHERE web_id = ?", (ID,)).fetchone() is not None:
            return True
        else:
            return False
        
    def get_new_id(self):
        """Get new ID for new web page, return the new ID ( max ID + 1 )"""
        try:
            return self.cursor.execute("SELECT MAX(web_id) FROM web_data").fetchone()[0] + 1
        except TypeError:
            return 1

    def update_reference_domain(self, list_of_domain):
        """Update each domain's reference count in the table reference_domain of main database"""
        for domain in list_of_domain:
            # if the domain already exists in the table, update the reference count
            if self.domain_exist_check(domain):
                self.cursor.execute("UPDATE reference_domain SET ref_count = ref_count + 1 WHERE domain_name = ?", (domain,))
            else:
                self.cursor.execute("INSERT INTO reference_domain VALUES (?, ?)", (domain, 1))
            self.conn.commit()

    def update_web_data(self, new_id, url, all_word, ref_to):
        """Update web_data table with new web page's information"""
        all_word_str = ",".join(all_word)
        ref_to_str = ",".join(ref_to)
        self.cursor.execute("INSERT INTO web_data VALUES (?, ?, ?, ?)", (new_id, url, all_word_str, ref_to_str))
        self.conn.commit()
        
    def update_inverted_index(self, web_id, word_list):
        """Update inverted_index table with new web page's information"""
        word_count = {}
        for word in word_list:
            word_count[word] = word_count.get(word, 0) + 1
        for word, count in word_count.items():
            self.cursor.execute(f"SELECT word, inverted_dict FROM inverted_index WHERE word = '{word}'")
            result = self.cursor.fetchone()
            if result:
                inverted_dict = eval(result[1])
                inverted_dict[web_id] = count
                inverted_dict = str(inverted_dict)
                self.cursor.execute(f"UPDATE inverted_index SET document_freq = '{len(inverted_dict)}', inverted_Dict = '{inverted_dict}' WHERE Word = '{word}'")
            else:
                self.cursor.execute(f"INSERT INTO inverted_index (word, document_freq, inverted_dict) VALUES ('{word}', 1, '{{{web_id}:{count}}}')")
        self.conn.commit()

    def update_search_cache(self, query_list, ID_list):
        """Update search_cache table with new query and ID list"""
        query_list_str = ",".join(query_list)
        ID_list_str = ",".join(ID_list)
        self.cursor.execute("INSERT INTO search_cache VALUES (?, ?)", (query_list_str, ID_list_str))
        self.conn.commit()

    # Remover Methods

    def remove_web_data(self, web_id):
        """Remove web page's information from web_data table"""
        self.cursor.execute("DELETE FROM web_data WHERE web_id = ?", (web_id,))
        self.conn.commit()
    
    # def remove_inverted_index(self, web_id, list_of_words):
    #     """modify inverted_index table when a web page is removed"""
    #     for word in list_of_words:
    #         self.cursor.execute("SELECT inverted_dict FROM inverted_index WHERE word=?", (word,))
    #         inverted_dict = eval(self.cursor.fetchone()[0])
    #         inverted_dict.pop(web_id)
    #         self.cursor.execute("UPDATE inverted_index SET document_freq=?, inverted_dict=? WHERE Word=?", (len(inverted_dict), str(inverted_dict), word))
    #         self.conn.commit()
    def remove_inverted_index(self, web_id, words):
        """Remove id from indexing and reduce docsfreq"""
        for word in words:
            self.cursor.execute("SELECT inverted_dict FROM inverted_index WHERE word=?", (word,))
            inverted_dict = eval(self.cursor.fetchone()[0])
            inverted_dict.pop(web_id, None)
            self.cursor.execute(f"UPDATE inverted_index SET document_freq=?, inverted_dict=? WHERE word=?", (len(inverted_dict), str(inverted_dict), word))
        self.conn.commit()

    def uncount_ref_domain(self, domain_list):
        """Uncount reference count of a domain when a web page is removed"""
        for domain in domain_list:
            self.cursor.execute(f"UPDATE reference_domain SET ref_count = ref_count - 1 WHERE domain_name = '{domain}'")
        self.conn.commit()

    def remove_relate_cache(self, term_list):
        """Check if term in the list is in cache, remove that cache row"""
        self.cursor.execute("SELECT query_list FROM search_cache")
        search_cache = self.cursor.fetchall()
        # check all row in column Query_List if contain any term in term_list, 
        # if yes, remove that row
        for row in search_cache:
            for term in term_list:
                if term in row[0]:
                    self.cursor.execute("DELETE FROM search_cache WHERE query_list=?", (row[0],))
                    self.conn.commit() 
        print("Cache is updated (Removed related term in cache)") 


    def fetch_data_by_url(self, url):
        """get data from row by url"""
        self.cursor.execute("SELECT web_id, URL, all_word, ref_to FROM web_data WHERE url=?", (url,))
        result = self.cursor.fetchone()
        if result:
            return {
                'Web_ID' : int(result[0]),
                'URL' : result[1],
                'All_Word' : result[2].split(','),
                'Ref_To' : result[3].split(',')
            }
        else:
            return None

    def fetch_data_by_id(self, web_id):
        """get data from row by id"""
        self.cursor.execute("SELECT web_id, url, all_word, ref_to FROM web_data WHERE web_id=?", (web_id,))
        result = self.cursor.fetchone()
        if result:
            return {
                'Web_ID' : int(result[0]),
                'URL' : result[1],
                'All_Word' : result[2].split(','),
                'Ref_To' : result[3].split(',')
            }
        else:
            return None