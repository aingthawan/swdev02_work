# unit test for rawKeeper_ELT.py
# ok for now Feb 14, 2023


import unittest
# import sqlite3
from rawKeeper_ELT import rawKeeper


class TestRawKeeper(unittest.TestCase):
    """Test rawKeeper class"""

    def setUp(self):
        """Create a database for testing"""
        # Create a database in memory
        self.rk = rawKeeper(':memory:')
        # Create a table for testing
        self.rk.insertRaw('http://example.com', 'raw content')

    def tearDown(self):
        self.rk.close()

    def test_insertRaw(self):
        """Test insertRaw() method"""
        # test insert a new row
        self.rk.insertRaw('http://example2.com', 'raw content2')

        # test insert an existing row
        result = self.rk.checkRaw('http://example2.com')

        # test insert a row with a different raw content
        self.assertIsNotNone(result)
        # test insert a row with a different raw content
        self.assertEqual(result[0], 'http://example2.com')

    def test_removeRaw(self):
        """Test removeRaw() method"""
        # test remove a row
        self.rk.removeRaw('http://example.com')
        # test that the row is removed
        result = self.rk.checkRaw('http://example.com')
        self.assertIsNone(result)

    def test_checkRaw(self):
        """Test checkRaw() method"""
        # test check a row
        result = self.rk.checkRaw('http://example.com')
        # test that the row is checked
        self.assertIsNotNone(result)
        self.assertEqual(result[0], 'http://example.com')

if __name__ == '__main__':
    unittest.main()
