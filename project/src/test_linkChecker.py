from linkChecker import *
import unittest
import unittest.mock
import requests
from urllib.parse import urlparse
import sqlite3

class TestLinkCheckers(unittest.TestCase):
    def setUp(self):
        # Create a dummy class that has the `alreadyScrape` method
        class DummyClass:
            def alreadyScrape(self, url_to_check):
                self.cursor = MagicMock()
                self.cursor.fetchone.return_value = None
                return False

        self.dummy = DummyClass()

    def test_already_scraped(self):
        self.dummy.cursor.fetchone.return_value = ('http://example.com')
        result = self.dummy.alreadyScrape('http://example.com')
        self.assertTrue(result)

    # def test_not_already_scraped(self):
    #     self.dummy.cursor.fetchone.return_value = None
    #     result = self.dummy.alreadyScrape('http://example.com')
    #     self.assertFalse(result)

    # def test_checkAccessibility(self):
    #     """Test the checkAccessibility method"""
    #     with unittest.mock.patch("requests.get") as mock_get:
    #         mock_response = unittest.mock.Mock()
    #         mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
    #         mock_get.return_value = mock_response
    #         # Test a bad response
    #         result = self.lc.checkAccessibility("https://www.example.com")
    #         self.assertFalse(result)
    #         # Test a good response
    #         mock_response.raise_for_status.side_effect = None
    #         result = self.lc.checkAccessibility("https://www.example.com")
    #         self.assertTrue(result)

    # def test_compareDomains(self):
    #     """Test the compareDomains method"""
    #     # Test the same domain
    #     result = self.lc.compareDomains("https://www.example.com", "https://www.example.com")
    #     self.assertTrue(result)

    #     # Test different domains
    #     result = self.lc.compareDomains("https://www.example.com", "https://www.example.org")
    #     self.assertFalse(result)

if __name__ == "__main__":
    unittest.main()
