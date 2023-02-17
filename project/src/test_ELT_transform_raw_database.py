import unittest
import sqlite3
import os
from ELT_transform import raw_database

class TestRawDatabase(unittest.TestCase):
    """Test raw_database class"""

    def setUp(self):
        # create a temporary database
        self.raw_db = raw_database('project\database\testing_database\raw_database_test.db')
        self.raw_db.create_table()
        self.raw_db.insert_row('https://www.example.com', 'This is some raw text.')

    # def tearDown(self):
        # os.remove('project\database\testing_database\raw_database_test.db')

    def test_get_row(self):
        # test get_row()
        self.assertEqual(self.raw_db.get_row(), ('https://www.example.com', 'This is some raw text.'))

    # def test_delete_row(self):

if __name__ == '__main__':
    unittest.main()
