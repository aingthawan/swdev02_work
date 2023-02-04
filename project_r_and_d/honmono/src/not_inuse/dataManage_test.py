import unittest
import sqlite3
from dataManage import data_manage

class TestDataManage(unittest.TestCase):
    def setUp(self):
        self.db_file = 'test.db'
        self.data = data_manage(self.db_file)
    
    def test_connect_db(self):
        self.assertIsInstance(self.data.conn, sqlite3.Connection)
        self.assertIsInstance(self.data.cursor, sqlite3.Cursor)
        
    def test_create_table(self):
        # check if tables are created
        self.data.cursor.execute("SELECT name from sqlite_master WHERE type='table'")
        tables = [table[0] for table in self.data.cursor.fetchall()]
        self.assertIn('webData', tables)
        self.assertIn('domainRef', tables)
        self.assertIn('invertedIndex', tables)
        
    def test_insert_webData(self):
        self.data.insert_webData('https://www.example.com')
        self.data.cursor.execute("SELECT * FROM webData")
        web_data = self.data.cursor.fetchone()
        self.assertEqual(web_data[1], 'https://www.example.com')
        
    def test_insert_domainRef(self):
        self.data.insert_domainRef('example.com', 5)
        self.data.cursor.execute("SELECT * FROM domainRef")
        domain_ref = self.data.cursor.fetchone()
        self.assertEqual(domain_ref[0], 'example.com')
        self.assertEqual(domain_ref[1], 5)
        
    def test_insert_invertedIndex(self):
        self.data.insert_invertedIndex('test', 2, {1: 2, 3: 4})
        self.data.cursor.execute("SELECT * FROM invertedIndex")
        inverted_index = self.data.cursor.fetchone()
        self.assertEqual(inverted_index[0], 'test')
        self.assertEqual(inverted_index[1], 2)
        self.assertEqual(json.loads(inverted_index[2]), {1: 2, 3: 4})
        
    # def test_remove_webData(self):
    #     self.data.insert_webData('https://www.example.com')
    #     self.data.remove_webData(1)
    #     self.data.cursor.execute("SELECT * FROM webData")
    #     self.assertEqual(self.data.cursor.fetchone(), None)
        
    # def test_remove_domainRef(self):
    #     self.data.insert_domainRef('example.com', 5)
    #     self.data.remove_domainRef('example.com')
    #     self.data.cursor.execute("SELECT * FROM domainRef")
    #     self.assertEqual(self.data.cursor.fetchone(), None)
        
    # def test_remove_invertedIndex(self):
    #     self.data.insert_invertedIndex('test', 2, {1: 2, 3: 4})
    #     self.data.remove_invertedIndex('test')
    #     self.data.cursor.execute("SELECT * FROM invertedIndex")
    #     self.assertEqual(self.data.cursor.fetchone(), None)

    # def tearDown(self):
    #     self.data.conn.close()
    #     if name == 'main':
    #         unittest.main()
