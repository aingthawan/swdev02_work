import unittest
import os
import sqlite3
from ELT_searching import invertedIndexSearch

class TestInvertedIndexSearch(unittest.TestCase):

    def setUp(self):
        self.path = "project/database/for_test/test_search_database.db"
        # remove the test file
        os.remove(self.path) if os.path.exists(self.path) else None
        # insert test data into the test database
        self.conn = sqlite3.connect(self.path)
        self.cursor = self.conn.cursor()
        
        # Create table for keeping domain name of url and times of referenced to
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        # Create a table for unique id for each url and list of all words in that url and list of url found on that page
        self.cursor.execute("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To, Place)")
        # Create table for each word, number of document that contain that word and dictionary of sorted key that are id of url and number of that word found on that link
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")
        # create table for keeping list of query and list of id that match with that query
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Search_Cache (Query_List TEXT, ID_List TEXT)""")
        
        # input some inverted index data
        self.cursor.execute("INSERT INTO Inverted_Index VALUES ('hello', 3, '{1: 1, 2: 2, 3: 3}')")
        self.cursor.execute("INSERT INTO Inverted_Index VALUES ('world', 3, '{1: 1, 2: 2, 3: 3}')")
        # input some web data
        self.cursor.execute("INSERT INTO web_Data VALUES (1, 'https://www.google1.com', 'hello world', 'https://www.google.com', {'country1': 1, 'country2': 2})")
        self.cursor.execute("INSERT INTO web_Data VALUES (2, 'https://www.google2.com', 'hello world', 'https://www.google.com', {'country3': 1})")
        self.cursor.execute("INSERT INTO web_Data VALUES (3, 'https://www.google3.com', 'hello world', 'https://www.google.com', {'country2': 1})")
        self.conn.commit()
        self.conn.close()
        
        self.search = invertedIndexSearch(self.path)

    def tearDown(self):
        self.search.close()

    def test_queryCleaner(self):
        # Test the queryCleaner method with a sample query
        query = "   Hello   World  "
        cleaned_query = self.search.queryCleaner(query)
        self.assertEqual(cleaned_query, ["hello", "world"])

    def test_getInvertedIndexDict(self):
        # Test the getInvertedIndexDict method with a sample word list
        word_list = ["hello", "world"]
        inverted_index_dict = self.search.getInvertedIndexDict(word_list)
        # self.assertIsNotNone(inverted_index_dict)
        self.assertEquals(inverted_index_dict, [[1, 2, 3], [1, 2, 3]])

    def test_get_common_id(self):
        # Test the get_common_id method with a sample list of lists
        lists = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        common_id_list = self.search.get_common_id(lists)
        self.assertListEqual(common_id_list, [3])


# main function
if __name__ == "__main__":
    unittest.main()