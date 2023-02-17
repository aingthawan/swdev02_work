# a file for searching url from database and return the ranked url

from cleanRawText import *

import sqlite3
import os

file_name = 'database_elt_test1.db'
database_file = 'project\database\\' + file_name

class invertedIndexSearch:
    """class for searching the url from database, Inverted Indexing Style"""

    def __init__(self, database_file):
        """initialize the database"""
        self.tc = TextCleaners()
        self.conn = sqlite3.connect(database_file)
        self.curr = self.conn.cursor()

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
        list_temp = []
        for word in word_list:
            self.curr.execute(f"SELECT * FROM Inverted_Index WHERE Word = '{word}'")
            dict_temp = self.curr.fetchone()
            list_temp.append( list(eval(dict_temp[2]).keys()) )
        return list_temp
            
    def get_common_id(self, lists):
        common_data = set(lists[0])
        for lst in lists[1:]:
            common_data.intersection_update(set(lst))
        return list(common_data)
    
    def search_full_process(self, user_query):
        """return a list of inverted index search web ID"""
        print("Searching Query : ", user_query)
        list_query = self.queryCleaner(user_query)
        print("Cleaned Query : ", list_query)
        temp_dict = self.getInvertedIndexDict(list_query)
        print("Results : ")
        return self.get_common_id(temp_dict)
        
        # return self.get_common_id(self.getInvertedIndexDict(self.queryCleaner(user_query)))
        
    def Link_from_ID(self, id_list):
        """return a url from id list"""
        temp_list = []
        for ids in id_list:
            self.curr.execute(f"SELECT URL FROM web_Data WHERE Web_ID = {ids}")
            text = self.curr.fetchone()
            temp_list.append(text)
            
        return temp_list

# main
if __name__ == "__main__":
    # make a loop for searching until user want to exit
    # using try and except for error handling keyboard interrupt to exit the program
    iis = invertedIndexSearch(database_file)

    try:
        while True:
            user_query = input("\n\nEnter your query : ")
            os.system('cls')
            a = iis.search_full_process(user_query)
            b = iis.Link_from_ID(a)
            for i in b:
                print(i[0])

    except KeyboardInterrupt:
        print("Exiting the program")
