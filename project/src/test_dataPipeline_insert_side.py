# file for unittest of dataPipeline.py
# Okay

import sqlite3
import unittest
import os
from dataPipeline import * 

class TestDataPipelines(unittest.TestCase):
    """Test class for the dataPipelines class."""

    def setUp(self):
        self.database_file = 'project/database/for_test/test_pipeline_database.db'
        self.dp = dataPipelines(self.database_file)

    def tearDown(self):
        self.dp.conn.close()
        # Delete the test database file
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Reference_Domain")
        cursor.execute("DROP TABLE IF EXISTS web_Data")
        cursor.execute("DROP TABLE IF EXISTS Inverted_Index")
        cursor.execute("DROP TABLE IF EXISTS Search_Cache")
        conn.commit()
        conn.close()
        # remove the test database file
        os.remove(self.database_file)
        
    def test_create_table(self):
        """Test that the database tables are created correctly."""
        self.cursor = self.dp.conn.cursor()
        # get the names of all tables in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        # check that the tables are created correctly
        self.assertIn(('Reference_Domain',), tables)
        self.assertIn(('web_Data',), tables)
        self.assertIn(('Inverted_Index',), tables)
        self.assertIn(('Search_Cache',), tables)

    def test_update_reference_domain(self):
        """Test that updateReferenceDomain() updates reference domain table correctly."""
        # execute updateReferenceDomain() with a list of reference domains
        self.dp.updateReferenceDomain(['example.com', 'google.com', 'example.com'])
        # check that the reference domain table is updated correctly
        self.cursor = self.dp.conn.cursor()
        self.cursor.execute("SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name='example.com'")
        ref_count = self.cursor.fetchone()[0]
        self.assertEqual(ref_count, 2)
        self.cursor.execute("SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name='google.com'")
        ref_count = self.cursor.fetchone()[0]
        self.assertEqual(ref_count, 1)

    def test_get_unique_id(self):
        """Test that getUniqueID() returns unique IDs for each website."""
        self.cursor = self.dp.conn.cursor()
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (1, 'example.com', 'example,com', 'google.com')")
        # already have one website in the database, so the next website should have ID 2
        self.assertEqual(self.dp.getUniqueID(), 2)
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (2, 'google.com', 'google,com', 'example.com')")
        # next website should have ID 3
        self.assertEqual(self.dp.getUniqueID(), 3)
        # should still return 3 if we try to get another unique ID
        self.assertEqual(self.dp.getUniqueID(), 3)
        
        
    # test updateWebData()
    def test_update_web_data(self):
        # test id, url, dict of all words, list of reference domains
        self.cursor = self.dp.conn.cursor()
        self.dp.updateWebData(191919, 'example.com', {'example': 1, 'com': 1}, ['google.com', 'facebook.com'])
        
        # check that the web_Data table is updated correctly
        self.cursor.execute("SELECT Web_ID FROM web_Data WHERE Web_ID=191919")
        self.assertEqual(self.cursor.fetchone()[0], 191919)
        self.cursor.execute("SELECT URL FROM web_Data WHERE Web_ID=191919")
        self.assertEqual(self.cursor.fetchone()[0], 'example.com')
        self.cursor.execute("SELECT All_Word FROM web_Data WHERE Web_ID=191919")
        self.assertEqual(self.cursor.fetchone()[0], 'example , com')
        self.cursor.execute("SELECT Ref_To FROM web_Data WHERE Web_ID=191919")
        self.assertEqual(self.cursor.fetchone()[0], 'google.com , facebook.com')
    
    # test fetch_data_by_id()
    def test_fetch_data_by_id(self):
        # expected result
        exp_dict = {
                'Web_ID' : 291919,
                'URL' : 'example.com',
                'All_Word' : ['example', 'com'],
                'Ref_To' : ['google.com', 'facebook.com']
            }
        # insert data into web_Data table
        self.dp.updateWebData(291919, 'example.com', {'example': 1, 'com': 1}, ['google.com', 'facebook.com'])
        # test method
        result = self.dp.fetch_data_by_id(291919)
        self.assertEqual(result, exp_dict)
        
    # test fetch_data_by_url()
    def test_fetch_data_by_url(self):
        # expected result
        exp_dict = {
                'Web_ID' : 391919,
                'URL' : 'example_url.com',
                'All_Word' : ['example', 'com'],
                'Ref_To' : ['google.com', 'facebook.com']
            }
        # insert data into web_Data table
        self.dp.updateWebData(391919, 'example_url.com', {'example': 1, 'com': 1}, ['google.com', 'facebook.com'])
        # test method
        result = self.dp.fetch_data_by_url('example_url.com')
        self.assertEqual(result, exp_dict)
        
    # test uncountRef()
    def test_uncountRef(self):
        # insert ref and count
        self.cursor = self.dp.conn.cursor()
        self.cursor.execute("INSERT INTO Reference_Domain (Domain_Name, Ref_Count) VALUES ('example1.com', 2)")
        self.cursor.execute("INSERT INTO Reference_Domain (Domain_Name, Ref_Count) VALUES ('example2.com', 10)")
        self.dp.uncountRef(['example1.com', 'example2.com'])
        # check that the reference domain table is updated correctly
        self.cursor.execute("SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name='example1.com'")
        self.assertEqual(self.cursor.fetchone()[0], 1)
        self.cursor.execute("SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name='example2.com'")
        self.assertEqual(self.cursor.fetchone()[0], 9)
        
    # test removeTermInCache()
    def test_removeTermInCache(self):
        # insert test data
        self.cursor = self.dp.conn.cursor()
        self.cursor.execute("INSERT INTO Search_Cache (Query_List, ID_List) VALUES ('example1', '[1, 2, 3]')")
        self.cursor.execute("INSERT INTO Search_Cache (Query_List, ID_List) VALUES ('example1,example3', '[1, 2, 3]')")
        self.cursor.execute("INSERT INTO Search_Cache (Query_List, ID_List) VALUES ('example3,example2', '[1, 2, 3]')")
        self.cursor.execute("INSERT INTO Search_Cache (Query_List, ID_List) VALUES ('example3', '[1, 2, 3]')")
        self.dp.removeTermInCache(['example1', 'example2'])
        # check theres is not any row contain example1 or example2
        self.cursor.execute("SELECT * FROM Search_Cache WHERE Query_List LIKE '%example1%'")
        self.assertEqual(self.cursor.fetchone(), None)
    
    # test updateInvertedIndex()
    def test_updateInvertedIndex(self):
        self.dp.updateInvertedIndexing(1, ['example1', 'example2', 'example2'])
        self.dp.updateInvertedIndexing(2, ['example1', 'example3'])
        self.dp.updateInvertedIndexing(3, ['example3', 'example2'])
        # test that the inverted index table is updated correctly
        self.cursor = self.dp.conn.cursor()
        # check Documant_Freq of word example1,2,3
        self.cursor.execute("SELECT Document_Freq FROM Inverted_Index WHERE Word='example1'")
        self.assertEqual(self.cursor.fetchone()[0], 2)
        self.cursor.execute("SELECT Document_Freq FROM Inverted_Index WHERE Word='example2'")
        self.assertEqual(self.cursor.fetchone()[0], 2)
        self.cursor.execute("SELECT Document_Freq FROM Inverted_Index WHERE Word='example3'")
        self.assertEqual(self.cursor.fetchone()[0], 2)
        # check inverted index of word example1,2,3
        self.cursor.execute("SELECT Inverted_Dict FROM Inverted_Index WHERE Word='example1'")
        self.assertEqual(self.cursor.fetchone()[0], '{1: 1, 2: 1}')
        self.cursor.execute("SELECT Inverted_Dict FROM Inverted_Index WHERE Word='example2'")
        self.assertEqual(self.cursor.fetchone()[0], '{1: 2, 3: 1}')
        self.cursor.execute("SELECT Inverted_Dict FROM Inverted_Index WHERE Word='example3'")
        self.assertEqual(self.cursor.fetchone()[0], '{2: 1, 3: 1}')
        

    

if __name__ == '__main__':
    unittest.main()
