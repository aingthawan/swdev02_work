# file for testing singleScrape.py
# okay for now, working fine
# date : Feb 19 ,2023

import unittest
from unittest.mock import patch, MagicMock
from singleScrape import *

class TestPageScrapers(unittest.TestCase):
    
    @patch('singleScrape.requests')
    def test_get_raw_html(self, mock_requests):
        """Test get_raw_html() method"""
        # Ref : https://www.pythontutorial.net/python-unit-testing/python-mock-requests/
        self.ps = pageScrapers()
        
        # Test a successful request
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'test'

        # specify the return value of the get() method
        mock_requests.get.return_value = mock_response
        # call method and test
        self.assertEqual(self.ps.get_raw_html("www.test.com"), 'test')

        # Test a failed request
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = 'test'

        mock_requests.get.return_value = mock_response
        self.assertEqual(self.ps.get_raw_html("www.test.com"), None)

    def test_scrape_raw_text(self):
        """Test scrape_raw_text() method"""
        self.ps = pageScrapers()
        # correct case
        self.assertEqual(self.ps.scrape_raw_text("<html><head><title>Test</title></head><body><p>Test</p></body></html>"), "TestTest")
        # incorrect case
        self.assertNotEqual(self.ps.scrape_raw_text("<html><head><title>Test</title></head><body><p>Test</p></body></html>"), "Test")

    def test_scrape_all_urls(self):
        """Test scrape_all_urls() method"""
        self.ps = pageScrapers()
        # correct case
        self.assertEqual(self.ps.scrape_all_urls('<html><body><a href="http://example.com">Link</a></body></html>'), ['http://example.com'])
        self.assertEqual(self.ps.scrape_all_urls('<html><body><a href="http://example.com">Link 1</a><a href="http://google.com">Link 2</a></body></html>'), ['http://google.com', 'http://example.com'])
        self.assertEqual(self.ps.scrape_all_urls('<html><body><a href="http://example.com/image.png">Link 1</a><a href="http://google.com/image.jpg">Link 2</a></body></html>'), [])
        # incorrect case
        self.assertNotEqual(self.ps.scrape_all_urls('<html><body><a href="http://example.com/image.png">Link 1</a><a href="http://google.com/image.jpg">Link 2</a></body></html>'), ['http://example.com/image.png', 'http://google.com/image.jpg'])

    # still error

    # @patch('singleScrape.requests')
    # def test_scrape_page(self, mock_requests):
    #     """Test scrape_page() method"""
    #     self.ps = pageScrapers()
    #     # correct case
    #     mock_response = MagicMock()
    #     mock_response.status_code = 200
    #     mock_response.text = "<html><body><p>This is some raw text.</p><a href='https://example.com'>Link to Example</a></body></html>"
    #     mock_requests.get.return_value = mock_response
    #     self.assertEqual(self.ps.scrape_page("https://example.com"), {"url": "https://example.com", "backlinks": ['https://example.com'], "rawText": "This is some raw text.Link to Example"})

if __name__ == '__main__':
    unittest.main()
