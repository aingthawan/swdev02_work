# file for unittest of dataPipeline.py
# developing

import sqlite3
import os
import unittest
from dataPipeline import *


class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        self.test_db_file = 'project/database/for_test/test_pipeline_database.db'
        self.data_pipeline = dataPipelines(self.test_db_file)
        self.data_pipeline.close()
        
        # connect to a database ,create a cursor , then insert test data
        self.conn = sqlite3.connect(self.test_db_file)
        self.cursor = self.conn.cursor()
        # insert test for removeInvertedIndex
        self.cursor.execute("INSERT INTO Inverted_Index (Word, Document_Freq, Inverted_Dict) VALUES (?, ?, ?)",
                            ('testword', 3, '{1:1, 2:2, 3:1}'))
        self.conn.commit()
        # insert test for removeWebData
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, ?, ?, ?)",
                            (1, 'https://www.example.com', 'example, website, test', 'https://www.google.com, https://www.yahoo.com'))
        self.conn.commit()
        self.conn.close()
        
        self.data_pipeline = dataPipelines(self.test_db_file)
        
        
    def tearDown(self):
        self.data_pipeline.conn.close()
        # os.remove(self.test_db_file)
    
    def test_removeWebData(self):
        # Create test data
        test_url = 'https://www.example.com'
        
        # Call the method being tested
        self.data_pipeline.removeWebData(test_url)
        
        # Check that the web_Data table was updated correctly
        self.data_pipeline.cursor.execute("SELECT * FROM web_Data WHERE URL=?", (test_url,))
        result = self.data_pipeline.cursor.fetchone()
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()
