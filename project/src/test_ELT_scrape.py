import unittest
from unittest.mock import Mock
from ELT_scrape import *
import os

# raw_database_file = 'project/database/test_raw_database.db'
# main_database_file = 'project/database/test_main_database.db'

class TestGetRawContent(unittest.TestCase):

    def setUp(self):
        self.raw_db_file = "project/database/for_test/test_raw_database.db"
        self.main_db_file = "project/database/for_test/test_main_database.db"
        self.grc = get_raw_content(self.raw_db_file, self.main_db_file)

    def test_get_domain(self):
        # case 1
        url = "https://example.com/path/to/page.html"
        domain = self.grc.get_domain(url)
        self.assertEqual(domain, "example.com")
        # case 2
        url = "https://www.example.com/path/to/page.html"
        domain = self.grc.get_domain(url)
        self.assertEqual(domain, "example.com")
        # case 3
        url = "https://es.example.com"
        domain = self.grc.get_domain(url)
        self.assertEqual(domain, "es.example.com")
        

    def test_crawl(self):
        url = "https://example.com"
        current_depth = 0
        limit_depth = 2
        self.grc.crawl(url, current_depth, limit_depth)
        # assert that the raw content for the url was inserted into the raw database
        #  check by calling the checkRaw method
        self.assertTrue(self.grc.rk.checkRaw(url))
        
    def tearDown(self):
        self.grc.close()
        # delete test database
        # os.remove(self.raw_db_file)
        # os.remove(self.main_db_file)

if __name__ == '__main__':
    unittest.main()
