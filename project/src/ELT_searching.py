# a file for searching url from database and return the ranked url

from cleanRawText import *
import sqlite3
import os
import math
import time

class invertedIndexSearch:
    """class for searching the url from database, Inverted Indexing Style"""

    def __init__(self, database_file):
        """initialize the database"""
        self.tc = TextCleaners()
        self.conn = sqlite3.connect(database_file, timeout=10)
        self.curr = self.conn.cursor()
        self.create_cache_table()

    def create_cache_table(self):
        """Create a table for caching the search result, Attribute : List of query, List of ID"""
        self.curr.execute("""CREATE TABLE IF NOT EXISTS Search_Cache (
            Query_List TEXT,
            ID_List TEXT
        )""")
        # self.conn.commit()

    def close(self):
        """close the database connection"""
        self.conn.close()

    # tested
    def queryCleaner(self, query):
        """clean the query from the user, return the clean query unrepeated list"""
        clean_query = self.tc.clean(query)
        # remove the repeated word
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
                self.curr.execute(f"SELECT * FROM Inverted_Index WHERE Word = '{word}'")
                dict_temp = self.curr.fetchone()
                list_temp.append( list(eval(dict_temp[2]).keys()) )
            return list_temp
        except:
            return None
    
    # tested        
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
            # start_time = time.time()
            temp_list = []
            for ids in id_list:
                self.curr.execute(f"SELECT URL FROM web_Data WHERE Web_ID = {ids}")
                text = self.curr.fetchone()
                temp_list.append(text)
            # end_time = time.time()
            # print("Link from ID Time : ", end_time - start_time, "\n")
            return temp_list
        else:
            return None
    
    def invertedIndexSearch(self, cleaned_user_query):
        """return a list of inverted index search web ID"""
        # get inverted index time
        start_time = time.time()
        temp = self.get_common_id(self.getInvertedIndexDict(cleaned_user_query))
        end_time = time.time()
        print("Inverted Index Search Time : ", end_time - start_time)
        # print("Total ", len(temp), " results found")
        return temp
    
    # def TFScore(self, word, IDlist):
    #     """return the TF score for each id in the id list to a term"""
    #     score_temp = {}
    #     # start_time = time.time()
    #     for ids in IDlist:
    #         # total word in the document
    #         total_words = len((self.curr.execute(f"SELECT All_Word FROM web_Data WHERE Web_ID = {ids}").fetchone()[0]).split(" , "))
    #         total_term = eval(self.curr.execute(f"SELECT Inverted_Dict FROM Inverted_Index WHERE Word = '{word}'").fetchone()[0])[ids]
    #         score_temp[ids] = total_term / total_words
    #     end_time = time.time()
    #     # print("TF Score Time : ", end_time - start_time)
    #     return score_temp
    def TFScore(self, word, IDlist):
        """return the TF score for each id in the id list to a term"""
        score_temp = {}
        inverted_dict = {}
        total_words_dict = {}
        # Get inverted dictionary and total word count for all documents in IDlist
        for ids in IDlist:
            doc_row = self.curr.execute(f"SELECT All_Word FROM web_Data WHERE Web_ID = {ids}").fetchone()
            total_words = len(doc_row[0].split(" , "))
            total_words_dict[ids] = total_words
            inverted_dict[ids] = eval(self.curr.execute(f"SELECT Inverted_Dict FROM Inverted_Index WHERE Word = '{word}'").fetchone()[0])
        # Calculate TF scores for each document in IDlist
        for ids in IDlist:
            score_temp[ids] = inverted_dict[ids][ids] / total_words_dict[ids]
        return score_temp

        

    # def IDFScore(self, word_list):
    #     """return the IDF score dictionary of each word in the word list"""
    #     # start_time = time.time()
    #     score_temp = {}
    #     for word in word_list:
    #         # get total document
    #         self.curr.execute("SELECT COUNT(*) FROM web_Data")
    #         total_doc = self.curr.fetchone()[0]
    #         # get total document contain the word
    #         self.curr.execute(f"SELECT Document_Freq FROM Inverted_Index WHERE Word = '{word}'")
    #         total_doc_contain = self.curr.fetchone()[0]
    #         score_temp[word] = math.log(total_doc / total_doc_contain)
    #     # end_time = time.time()
    #     # print("IDF Score Time : ", end_time - start_time)
    #     return score_temp
    def IDFScore(self, word_list):
        score_temp = {}
        self.curr.execute("SELECT COUNT(*) FROM web_Data")
        total_doc = self.curr.fetchone()[0]
        word_freq_query = "SELECT Word, Document_Freq FROM Inverted_Index WHERE Word IN ({})".format(','.join(['?'] * len(word_list)))
        self.curr.execute(word_freq_query, word_list)
        word_freqs = dict(self.curr.fetchall())
        for word in word_list:
            total_doc_contain = word_freqs.get(word, 0)
            score_temp[word] = math.log(total_doc / total_doc_contain) if total_doc_contain > 0 else 0
        return score_temp



    # Version 2
    def TFIDFRank(self, word_list, IDlist):
        """return the ranked ID list from the TF-IDF score"""
        # time for TF-IDF
        start_time = time.time()
        # get total document count
        self.curr.execute("SELECT COUNT(*) FROM web_Data")
        total_doc = self.curr.fetchone()[0]
        # get document frequency for all words in the word list
        word_idf_dict = {}
        for word in word_list:
            self.curr.execute(f"SELECT Document_Freq FROM Inverted_Index WHERE Word = '{word}'")
            total_doc_contain = self.curr.fetchone()[0]
            word_idf_dict[word] = math.log(total_doc / total_doc_contain)
        # calculate the TF-IDF score for all documents in the ID list
        final_score_dict = {}
        for ids in IDlist:
            final_score_dict[ids] = 0
            total_words = len((self.curr.execute(f"SELECT All_Word FROM web_Data WHERE Web_ID = {ids}").fetchone()[0]).split(" , "))
            for word in word_list:
                total_term = eval(self.curr.execute(f"SELECT Inverted_Dict FROM Inverted_Index WHERE Word = '{word}'").fetchone()[0])[ids]
                final_score_dict[ids] += (total_term / total_words) * word_idf_dict[word]
        # sort the final score dictionary descending
        sorted_final_score_dict = {k: v for k, v in sorted(final_score_dict.items(), key=lambda item: item[1], reverse=True)}
        end_time = time.time()
        print(" New TF-IDF Ranking Time : ", end_time - start_time)
        return sorted_final_score_dict.keys()
    
    
    def compare_query(self, list1, list2):
        """Method for comparing two list of words, True if equal, False if not equal."""
        # check if all word in list1 is in list2
        # return True if all word in list1 is in list2
        if len(list1) == len(list2):
            for word in list1:
                if word not in list2:
                    return False
            return True
        else:
            return False
    
    # a method to cache the result
    def search_cacher(self, user_query, id_list):
        """Method for caching the result of the search"""
        # insert query and result list to the cache table
        self.curr.execute(f"INSERT INTO Search_Cache (Query_List, ID_List) VALUES ('{user_query}', '{id_list}')")
        self.conn.commit()
        
    # method to check if the query is in the cache
    # def search_cache_checker(self, cleaned_query):
    #     # check if the query is in the Query_List column
    #     # if yes return the ID_List
    #     self.curr.execute("SELECT Query_List FROM Search_Cache")
    #     search_cache = self.curr.fetchall()
    #     for item in search_cache:
    #         if self.compare_query(cleaned_query, item[0].split(",")):
    #             # if the query is in the cache, return the result
    #             self.curr.execute("SELECT ID_List FROM Search_Cache WHERE Query_List = ?", (item[0],))
    #             return eval(self.curr.fetchone()[0])
    #         # else return None
    #         else:
    #             continue
    #     # out of the loop, return None
    #     return None
    def search_cache_checker(self, cleaned_query):
        # check if the query is in the Query_List column
        # if yes return the ID_List
        self.curr.execute("SELECT ID_List FROM Search_Cache WHERE Query_List = ?", (",".join(cleaned_query),))
        result = self.curr.fetchone()
        if result is not None:
            return eval(result[0])
        # out of the loop, return None
        return None



    def full_search(self, user_query):
        """return a list of url from a user query"""
        cleaned_query = self.queryCleaner(user_query)
        if cleaned_query != None:
            # check if the query is in the cache
            load_from_cache = self.search_cache_checker(cleaned_query)
            if load_from_cache == None:
                # not in cache, search the query
                id_list = self.invertedIndexSearch(cleaned_query)
                # get a list of ranked url
                if id_list != None:
                    # return self.Link_from_ID(id_list)
                    # return the result and cache the result
                    self.search_cacher(",".join(cleaned_query), id_list)
                    return self.Link_from_ID(id_list)
                else:
                    return None            
            else:
                print("From Cache")
                # ================================================
                return self.Link_from_ID(load_from_cache) 
                # print(load_from_cache)
        else:
            return None
        

        

# main
if __name__ == "__main__":

    os.system('cls')
    print("\nWelcome to the Search Engine\nSetting up . . .\n\n")
    file_name = 'database_elt_main_small.db'
    database_file = 'project\\database\\for_dev\\' + file_name
    # make a loop for searching until user want to exit
    # using try and except for error handling keyboard interrupt to exit the program
    iis = invertedIndexSearch(database_file)
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
