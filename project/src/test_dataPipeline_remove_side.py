# developing

import sqlite3
import os
import unittest
from dataPipeline import * 


class TestDataPipeline(unittest.TestCase):
    
    def setUp(self):
        self.test_db_file = 'test.db'
        self.data_pipeline = dataPipelines(self.test_db_file)
        
    def tearDown(self):
        self.data_pipeline.conn.close()
        os.remove(self.test_db_file)
        
    def test_removeInvertedIndex(self):
        # Create test data
        test_word = 'test_word'
        test_web_id = 1
        test_inverted_dict = {'1': 1, '2': 2, '3': 1}
        test_doc_freq = 3
        self.data_pipeline.cursor.execute("INSERT INTO Inverted_Index (Word, Document_Freq, Inverted_Dict) VALUES (?, ?, ?)",
                                          (test_word, test_doc_freq, str(test_inverted_dict)))
        self.data_pipeline.conn.commit()
        
        # Call the method being tested
        self.data_pipeline.removeInvertedIndex(test_web_id, [test_word])
        
        # Check that the Inverted_Index table was updated correctly
        self.data_pipeline.cursor.execute("SELECT Document_Freq, Inverted_Dict FROM Inverted_Index WHERE Word=?", (test_word,))
        result = self.data_pipeline.cursor.fetchone()
        expected_inverted_dict = {'2': 2, '3': 1}
        expected_doc_freq = 2
        self.assertEqual(result[0], expected_doc_freq)
        self.assertEqual(ast.literal_eval(result[1]), expected_inverted_dict)
        
    def test_removeWebData(self):
        # Create test data
        test_web_id = 1
        test_url = 'https://www.example.com'
        test_all_word = 'example, website, test'
        test_ref_to = 'https://www.google.com, https://www.yahoo.com'
        self.data_pipeline.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, ?, ?, ?)",
                                          (test_web_id, test_url, test_all_word, test_ref_to))
        self.data_pipeline.conn.commit()
        
        # Call the method being tested
        self.data_pipeline.removeWebData(test_url)
        
        # Check that the web_Data table was updated correctly
        self.data_pipeline.cursor.execute("SELECT * FROM web_Data WHERE URL=?", (test_url,))
        result = self.data_pipeline.cursor.fetchone()
        self.assertIsNone(result)
        
if __name__ == '__main__':
    unittest.main()
