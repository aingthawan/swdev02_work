import unittest

class TestPageScrapers(unittest.TestCase):
    def setUp(self):
        self.scraper = pageScrapers()

    def test_get_raw_html(self):
        # Test a valid URL
        url = "https://www.example.com"
        result = self.scraper.get_raw_html(url)
        self.assertEqual(result.status_code, 200)

        # Test an invalid URL
        url = "https://www.example.invalid"
        result = self.scraper.get_raw_html(url)
        self.assertIsNone(result)

    def test_scrape_raw_text(self):
        html = "<html><body><p>Hello World</p></body></html>"
        result = self.scraper.scrape_raw_text(html)
        self.assertEqual(result, "Hello World")

    def test_scrape_all_urls(self):
        html = "<html><body><a href='https://www.example.com'>Example</a><a href='https://www.example.org'>Example 2</a><a href='https://www.example.com'>Example</a></body></html>"
        result = self.scraper.scrape_all_urls(html)
        self.assertEqual(result, ["https://www.example.com", "https://www.example.org"])

    def test_scrape_page(self):
        url = "https://www.example.com"
        result = self.scraper.scrape_page(url)
        self.assertIn("url", result)
        self.assertIn("backlinks", result)
        self.assertIn("rawText", result)

if __name__ == '__main__':
    unittest.main()
