# file for testing the raw database class in ELT_transform.py
# okay 

import unittest
import sqlite3
import os
from ELT_transform import raw_database

class TestRawDatabase(unittest.TestCase):

    def setUp(self):
        """set up the test"""
        self.db_name = 'project/database/for_test/test.db'
        self.conn = sqlite3.connect(self.db_name)
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE rawMaterial (id INTEGER PRIMARY KEY, url TEXT)''')
        self.cur.execute('''INSERT INTO rawMaterial(url) VALUES ('http://example.com')''')
        self.conn.commit()
        self.db = raw_database(self.db_name)

    def test_get_row(self):
        """test the get_row method"""
        # try get existing row
        row = self.db.get_row()
        self.assertIsNotNone(row)
        self.assertEqual(row[1], 'http://example.com')
        
    def test_delete_row(self):
        """test the delete_row method"""
        self.db.delete_row('http://example.com')
        self.cur.execute("SELECT * FROM rawMaterial WHERE url = 'http://example.com'")
        # table should be empty and return None
        row = self.cur.fetchone()
        self.assertIsNone(row)

    def tearDown(self):
        """clean up after the test"""
        self.db.close()
        self.conn.close()
        os.remove(self.db_name)

if __name__ == '__main__':
    unittest.main()
