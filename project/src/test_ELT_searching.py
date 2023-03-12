import unittest
import os
import sqlite3
from ELT_searching import invertedIndexSearch

class TestInvertedIndexSearch(unittest.TestCase):

    def setUp(self):
        self.path = "project/database/for_test/test_search_database.db"
        self.search = invertedIndexSearch(self.path)
        
    def test_create_database(self):
        self.search.create_cache_table()
        conn = sqlite3.connect(self.path)
        curr = conn.cursor()
        # get all the table names
        table_names = curr.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        conn.close()
        # check if the table is created
        self.assertIn(("Search_Cache",), table_names)

    def test_queryCleaner(self):
        # Test the queryCleaner method with a sample query
        query = "   Hello  ,/ World  "
        cleaned_query = self.search.queryCleaner(query)
        self.assertEqual(cleaned_query, ["hello", "world"])
        self.assertNotEqual(cleaned_query, ["Hello", "World"])
        self.assertNotEqual(cleaned_query, ["hello", "world", " "])        

    def test_get_common_id(self):
        # Test the get_common_id method with a sample list of lists
        lists = [[1, 2, 3], [2, 3, 4], [3, 4, 5]]
        common_id_list = self.search.get_common_id(lists)
        self.assertListEqual(common_id_list, [3])
        lists = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [1, 2, 3, 4, 5]]
        common_id_list = self.search.get_common_id(lists)
        self.assertListEqual(common_id_list, [3])

    def tearDown(self):
        self.search.close()
        # remove the test file
        os.remove(self.path)


# main function
if __name__ == "__main__":
    unittest.main()