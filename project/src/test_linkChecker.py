# make a test for the linkChecker.py
# one nonfunctioning test method left, continue to work on it

from linkChecker import *
import sqlite3
import unittest
from unittest.mock import patch, Mock
import os

class TestLinkCheckers(unittest.TestCase):
    def setUp(self):
        self.database_file = 'project/database/for_test/test_linkChecker_database.db'
        # remove test database file if it exists
        try:
            os.remove(self.database_file)
        except OSError:
            pass
        conn = sqlite3.connect(self.database_file)
        curr = conn.cursor()
        # create Web_Data table
        curr.execute("CREATE TABLE IF NOT EXISTS Web_Data(Web_ID, URL, All_Word, Ref_To)")
        # insert some data for testing to Web_Data table
        curr.execute("INSERT INTO Web_Data VALUES (1, 'https://www.example.com', 'example', 'https://www.example.com')")
        conn.commit()
        conn.close()
        self.link_checkers = LinkCheckers(self.database_file)
        
    def test_alreadyScrape(self):
        self.assertTrue(self.link_checkers.alreadyScrape('https://www.example.com'))
        self.assertFalse(self.link_checkers.alreadyScrape('https://www.example2.com'))

    def tearDown(self):
        self.link_checkers.close()
    
    # def test_createTable(self):
    #     # Test that tables are created
    #     conn = sqlite3.connect(self.database_file)
    #     # check that the tables are created correctly
    #     reference_domain_table = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Reference_Domain'")
    #     web_data_table = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='web_Data'")
    #     inverted_index_table = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Inverted_Index'")
    #     # assert that the tables are created
    #     self.assertIsNotNone(reference_domain_table.fetchone())
    #     self.assertIsNotNone(web_data_table.fetchone())
    #     self.assertIsNotNone(inverted_index_table.fetchone())
    #     conn.close()

    # @patch('link_checkers.requests.get')
    # def test_checkAccessibility(self, mock_requests_get):
    #     # Test that checkAccessibility returns True when a valid URL is provided
    #     mock_response = Mock()
    #     mock_response.status_code = 200
    #     mock_requests_get.return_value = mock_response
    #     url = 'https://www.example.com'
    #     result = self.link_checkers.checkAccessibility(url)
    #     self.assertTrue(result)

    #     # Test that checkAccessibility returns False when an invalid URL is provided
    #     mock_requests_get.side_effect = requests.exceptions.RequestException
    #     url = 'https://www.invalidurl.com'
    #     result = self.link_checkers.checkAccessibility(url)
    #     self.assertFalse(result)

    def test_get_domain(self):
        # Test that get_domain returns the correct domain name for a given URL
        url = 'https://www.example.com'
        result = self.link_checkers.get_domain(url)
        self.assertEqual(result, 'example')
        
        url = 'https://www.example.com'
        result = self.link_checkers.get_domain(url)
        self.assertNotEqual(result, 'www.example')
        

    def test_compareDomains(self):
        # Test that compareDomains returns True when two URLs have the same domain
        url1 = 'https://www.example.com'
        url2 = 'https://subdomain.example.com'
        result = self.link_checkers.compareDomains(url1, url2)
        self.assertTrue(result)

        # Test that compareDomains returns False when two URLs have different domains
        url1 = 'https://www.example.com'
        url2 = 'https://www.google.com'
        result = self.link_checkers.compareDomains(url1, url2)
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()