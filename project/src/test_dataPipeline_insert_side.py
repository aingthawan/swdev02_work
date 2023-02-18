# Okay for now, but need to add more tests?

import sqlite3
import unittest
from dataPipeline import * 

class TestDataPipelines(unittest.TestCase):
    """Test class for the dataPipelines class."""

    def setUp(self):
        self.database_file = 'project/database/test_database.db'
        self.dp = dataPipelines(self.database_file)

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

    def tearDown(self):
        self.dp.conn.close()
        # Delete the test database file
        conn = sqlite3.connect(self.database_file)
        cursor = conn.cursor()
        cursor.execute("DROP TABLE IF EXISTS Reference_Domain")
        cursor.execute("DROP TABLE IF EXISTS web_Data")
        cursor.execute("DROP TABLE IF EXISTS Inverted_Index")
        conn.commit()
        conn.close()

if __name__ == '__main__':
    unittest.main()
