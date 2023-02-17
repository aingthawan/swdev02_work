import unittest
import sqlite3

from dataPipeline import * 

class TestDataPipelines(unittest.TestCase):

    def setUp(self):
        self.pipeline = dataPipelines("test_db.sqlite3")
        self.conn = sqlite3.connect("test_db.sqlite3")
        self.cursor = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_createTable(self):
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        self.assertEqual(len(tables), 3)
        self.assertIn(("Reference_Domain",), tables)
        self.assertIn(("web_Data",), tables)
        self.assertIn(("Inverted_Index",), tables)

    def test_uncountRef(self):
        self.cursor.execute("INSERT INTO Reference_Domain (Domain_Name, Ref_Count) VALUES (?, 1)", ("example.com",))
        self.pipeline.uncountRef(["example.com"])
        self.cursor.execute("SELECT Ref_Count FROM Reference_Domain WHERE Domain_Name='example.com'")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 0)

    def test_removeInvertedIndex(self):
        self.cursor.execute("INSERT INTO Inverted_Index (Word, Document_Freq, Inverted_Dict) VALUES (?, 1, '{1: 1}')", ("example",))
        self.pipeline.removeInvertedIndex(1, ["example"])
        self.cursor.execute("SELECT Document_Freq FROM Inverted_Index WHERE Word='example'")
        result = self.cursor.fetchone()[0]
        self.assertEqual(result, 0)

    def test_removeWebData(self):
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, 'example.com', 'words', 'ref_to')", (1,))
        self.pipeline.removeWebData("example.com")
        self.cursor.execute("SELECT URL FROM web_Data WHERE URL='example.com'")
        result = self.cursor.fetchone()
        self.assertIsNone(result)

    def test_getUniqueID(self):
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, 'example.com', 'words', 'ref_to')", (1,))
        result = self.pipeline.getUniqueID()
        self.assertEqual(result, 2)

    def test_fetch_data_by_url(self):
        self.cursor.execute("INSERT INTO web_Data (Web_ID, URL, All_Word, Ref_To) VALUES (?, 'example.com', 'words', 'ref_to')", (1
