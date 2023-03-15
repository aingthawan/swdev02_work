from text_processor import *
import sqlite3
import os
import math
import time

class invertedIndexSearch:
    """class for searching the url from database, Inverted Indexing Style"""

    def __init__(self, database_file):
        """initialize the database"""
        self.tc = text_processor()
        self.conn = sqlite3.connect(database_file)
        self.curr = self.conn.cursor()
        self.create_cache_table()

    def close(self):
        """close the database connection"""
        self.conn.close()

    def create_cache_table(self):
        """Create a table for caching the search result, Attribute : List of query, List of ID"""
        self.curr.execute("""CREATE TABLE IF NOT EXISTS search_cache (
            query_list TEXT,
            id_list TEXT
        )""")
        self.conn.commit()

    def queryCleaner(self, query):
        """clean the query from the user, return the clean query unrepeated list"""
        clean_query = self.tc.clean(query)

        non_repeated_query = []
        for word in clean_query:
            if word not in non_repeated_query:
                non_repeated_query.append(word)
        return non_repeated_query

    def getInvertedIndexDict(self, word_list):
        """return a list of inverted index dictionary from a list of word"""
        list_temp = []
        try:
            for word in word_list:
                self.curr.execute(f"SELECT * FROM inverted_index WHERE word = '{word}'")
                dict_temp = self.curr.fetchone()
                list_temp.append( list(eval(dict_temp[2]).keys()) )
            return list_temp
        except:
            return None

    def get_common_id(self, lists):
        """return a list of common id from a list of list of id"""
        try:
            common_data = set(lists[0])
            for lst in lists[1:]:
                common_data.intersection_update(set(lst))
            return list(common_data)
        except:
            return None

    def Link_from_ID(self, id_list):
        """return a url from id list"""
        if id_list != None:

            temp_list = []
            for ids in id_list:
                self.curr.execute(f"SELECT URL FROM web_data WHERE web_id = {ids}")
                text = self.curr.fetchone()
                temp_list.append(text)

            return temp_list
        else:
            return None

    def invertedIndexSearch(self, cleaned_user_query):
        """return a list of inverted index search web ID"""

        start_time = time.time()
        temp = self.get_common_id(self.getInvertedIndexDict(cleaned_user_query))
        end_time = time.time()
        print("Inverted Index Search Time : ", end_time - start_time)

        return temp

    def TFScore(self, word, IDlist):
        """return the TF score for each id in the id list to a term"""
        score_temp = {}
        inverted_dict = {}
        total_words_dict = {}

        for ids in IDlist:
            doc_row = self.curr.execute(f"SELECT all_word FROM web_data WHERE web_id = {ids}").fetchone()
            total_words = len(doc_row[0].split(" , "))
            total_words_dict[ids] = total_words
            inverted_dict[ids] = eval(self.curr.execute(f"SELECT inverted_dict FROM inverted_index WHERE word = '{word}'").fetchone()[0])

        for ids in IDlist:
            score_temp[ids] = inverted_dict[ids][ids] / total_words_dict[ids]
        return score_temp

    def IDFScore(self, word_list):
        """return the IDF score for each term in the word list"""
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

        start_time = time.time()

        self.curr.execute("SELECT COUNT(*) FROM web_data")
        total_doc = self.curr.fetchone()[0]

        word_idf_dict = {}
        for word in word_list:
            self.curr.execute(f"SELECT document_freq FROM inverted_index WHERE word = '{word}'")
            total_doc_contain = self.curr.fetchone()[0]
            word_idf_dict[word] = math.log(total_doc / total_doc_contain)

        final_score_dict = {}
        for ids in IDlist:
            final_score_dict[ids] = 0
            total_words = len((self.curr.execute(f"SELECT all_word FROM web_data WHERE web_id = {ids}").fetchone()[0]).split(","))
            for word in word_list:
                total_term = eval(self.curr.execute(f"SELECT inverted_dict FROM inverted_index WHERE word = '{word}'").fetchone()[0])[ids]
                final_score_dict[ids] += (total_term / total_words) * word_idf_dict[word]

        sorted_final_score_dict = {k: v for k, v in sorted(final_score_dict.items(), key=lambda item: item[1], reverse=True)}
        end_time = time.time()
        print(" New TF-IDF Ranking Time : ", end_time - start_time)
        return sorted_final_score_dict.keys()

    def compare_query(self, list1, list2):
        """Method for comparing two list of words, True if equal, False if not equal."""

        if len(list1) == len(list2):
            for word in list1:
                if word not in list2:
                    return False
            return True
        else:
            return False

    def search_cacher(self, user_query, id_list):
        """Method for caching the result of the search"""
        self.curr.execute(f"INSERT INTO search_cache (query_list, id_list) VALUES ('{user_query}', '{id_list}')")
        self.conn.commit()

    def search_cache_checker(self, cleaned_query):
        """Method for checking if the search result is cached"""
        self.curr.execute("SELECT id_list FROM search_cache WHERE query_list = ?", (",".join(cleaned_query),))
        result = self.curr.fetchone()
        if result is not None:
            return eval(result[0])

        return None

    def full_search(self, user_query):
        """return a list of url from a user query"""
        cleaned_query = self.queryCleaner(user_query)
        print("Cleaned Search Query", cleaned_query)
        if cleaned_query != None:

            load_from_cache = self.search_cache_checker(cleaned_query)
            if load_from_cache == None:

                id_list = self.invertedIndexSearch(cleaned_query)

                if id_list != None:

                    self.search_cacher(",".join(cleaned_query), id_list)
                    return self.Link_from_ID(id_list)
                else:
                    return None            
            else:
                print("From Cache")

                return self.Link_from_ID(load_from_cache) 

        else:
            return None

if __name__ == "__main__":

    os.system('cls')
    print("\nWelcome to the Search Engine\nSetting up . . .\n\n")

    iis = invertedIndexSearch("organize\src\database\main_test.db")
    os.system('cls')

    try:
        while True:
            user_query = input("\n\nEnter your search query : ")
            os.system('cls')
            result_list = iis.full_search(user_query)
            if result_list == None:
                print("No result found")
            else:
                for result in result_list[:9]:
                    print(result[0])

    except KeyboardInterrupt:
        os.system('cls')
        iis.close()
        print("\n\n\t~ Quit program ~\n\n")