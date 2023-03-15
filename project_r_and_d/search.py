# a file for searching url from database and return the ranked url

from text_processor import text_processor
import sqlite3
import os
import math
import time

class spaida_search:
    """class for searching the url from database, Inverted Indexing Style"""

    def __init__(self, database_file):
        """initialize the database"""
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.curr = self.conn.cursor()
        self.tp = text_processor()
        self.create_cache_table()
        
    def close(self):
        """close the database connection"""
        self.conn.commit()
        self.conn.close()

    def create_cache_table(self):
        """Create a table for caching the search result, Attribute : List of query, List of ID"""
        self.curr.execute("""CREATE TABLE IF NOT EXISTS search_cache (
            query_list TEXT,
            id_list TEXT
        )""")
        self.conn.commit()

    def get_inverted_index(self, word_list):
        """Return the list of dict of the words, None if not found any word"""
        temp_list = []
        for word in word_list:
            self.curr.execute(f"SELECT * FROM inverted_index WHERE word = '{word}'")
            try:                
                dict_temp = self.curr.fetchone()
            except:
                return None
            temp_list.append(eval(dict_temp[2]))
        return temp_list
        
    def inverted_index_retrieval(self, dict_list):
        """Return the list of ID that contain all the words in the word list"""
        lists = []
        for dict in dict_list:
            lists.append(dict.keys())
        try:
            common_data = set(lists[0])
            for lst in lists[1:]:
                common_data.intersection_update(set(lst))
            return list(common_data)
        except:
            return None
        


    def TFScore(self, word, IDlist):
        """return the TF score for each id in the id list to a term"""
        score_temp = {}
        inverted_dict = {}
        total_words_dict = {}
        # Get inverted dictionary and total word count for all documents in IDlist
        for ids in IDlist:
            doc_row = self.curr.execute(f"SELECT all_word FROM web_data WHERE web_id = {ids}").fetchone()
            total_words = len(doc_row[0].split(" , "))
            total_words_dict[ids] = total_words
            inverted_dict[ids] = eval(self.curr.execute(f"SELECT inverted_dict FROM inverted_index WHERE word = '{word}'").fetchone()[0])
        # Calculate TF scores for each document in IDlist
        for ids in IDlist:
            score_temp[ids] = inverted_dict[ids][ids] / total_words_dict[ids]
        return score_temp
        
    def IDFScore(self, word_list):
        """return the IDF score for each word in the word list as a dict"""
        score_temp = {}
        self.curr.execute("SELECT COUNT(*) FROM web_data")
        total_doc = self.curr.fetchone()[0]
        word_freq_query = "SELECT word, document_freq FROM inverted_index WHERE word IN ({})".format(','.join(['?'] * len(word_list)))
        self.curr.execute(word_freq_query, word_list)
        word_freqs = dict(self.curr.fetchall())
        for word in word_list:
            total_doc_contain = word_freqs.get(word, 0)
            score_temp[word] = math.log(total_doc / total_doc_contain) if total_doc_contain > 0 else 0
        return score_temp

    def TFIDFRank(self, word_list, IDlist):
        """return the ranked ID list from the TF-IDF score"""
        # time for TF-IDF
        start_time = time.time()
        # get total document count
        self.curr.execute("SELECT COUNT(*) FROM web_data")
        total_doc = self.curr.fetchone()[0]
        # get document frequency for all words in the word list
        word_idf_dict = {}
        for word in word_list:
            self.curr.execute(f"SELECT document_freq FROM inverted_index WHERE word = '{word}'")
            total_doc_contain = self.curr.fetchone()[0]
            word_idf_dict[word] = math.log(total_doc / total_doc_contain)
        # calculate the TF-IDF score for all documents in the ID list
        final_score_dict = {}
        for ids in IDlist:
            final_score_dict[ids] = 0
            total_words = len((self.curr.execute(f"SELECT all_word FROM web_data WHERE web_id = {ids}").fetchone()[0]).split(" , "))
            for word in word_list:
                total_term = eval(self.curr.execute(f"SELECT inverted_dict FROM inverted_index WHERE word = '{word}'").fetchone()[0])[ids]
                final_score_dict[ids] += (total_term / total_words) * word_idf_dict[word]
        # sort the final score dictionary descending
        sorted_final_score_dict = {k: v for k, v in sorted(final_score_dict.items(), key=lambda item: item[1], reverse=True)}
        end_time = time.time()
        print(" New TF-IDF Ranking Time : ", end_time - start_time)
        return sorted_final_score_dict.keys()

    def full_search(self, query):
        """return the list of result from the query"""
        # get the list of query
        query_list = self.tp.clean(query)
        if query_list is not None:
            # get the list of id from the inverted index
            id_list = self.get_inverted_index(query_list)
            if id_list is not None:
                # get the list of id that contain all the words in the word list
                id_list = self.inverted_index_retrieval(id_list)
                # get the TF-IDF score for all the documents in the id list
                id_list = self.TFIDFRank(query_list, id_list)
                # return the list of result
                return id_list
            else:
                return None
        else:
            return None

# main
if __name__ == "__main__":

    os.system('cls')
    print("\nWelcome to the Search Engine\nSetting up . . .\n\n")
    ss = spaida_search("organize\\src\\database\\main_test.db")
    os.system('cls')
    
    try:
        while True:
            user_query = input("\n\nEnter your search query : ")
            os.system('cls')
            result_list = ss.full_search(user_query)
            if result_list == None:
                print("No result found")
            else:
                for result in result_list:
                    print(result[0])
        

    except KeyboardInterrupt:
        os.system('cls')
        ss.close()
        print("\n\n\t~ Quit program ~\n\n")
