from ELT_transform import main_database
import unittest
from unittest.mock import patch
import tempfile
import os


class TestMainDatabase(unittest.TestCase):

    def setUp(self):
        """set up the test"""
        self.db_name = 'project/database/test_TestMainDatabase.db'
        self.db = main_database(self.db_name)
        self.raw_content = '<!DOCTYPE html><html><head>	<title>Sample Page</title></head><body>	<h1>Heading 1</h1>	<p>This is a sample paragraph.</p>	<ul>		<li>List item 1</li>		<li><a href="https://www.example.com">Example website</a></li>		<li>List item 3</li>	</ul></body></html>'
        self.url = 'https://www.example2.com/'
        
    def test_get_domain(self):
        """test the get_domain method"""
        domain = self.db.get_domain('https://www.example.com/')
        self.assertEqual(domain, 'example.com')
        domain = self.db.get_domain('https://sub.example.com/')
        self.assertEqual(domain, 'sub.example.com')

    def test_updateLink(self):
        """test the updateLink method"""
        
        # raw html content for testing
        
        self.db.updateLink(self.url, self.raw_content)

        # assert that data is inserted correctly in the database
        web_data = self.db.dp.fetch_data_by_url(self.url)
        self.assertIsNotNone(web_data)
        self.assertEqual(web_data['URL'], self.url)
        self.assertEqual(web_data['All_Word'], ['sample', 'paragraph', 'head', '1'])
        self.assertListEqual(web_data['Ref_To'], ['example.com'])

        # remove the inserted data
        self.db.removeData(self.url)

    def test_removeData(self):
        """test the removeData method"""
        # raw html content for testing
        self.db.updateLink(self.url, self.raw_content)

        # assert that data is inserted correctly in the database
        web_data = self.db.dp.fetch_data_by_url(self.url)
        self.assertIsNotNone(web_data)

        # remove the inserted data
        self.db.removeData(self.url)

        # assert that data is removed from the database
        web_data = self.db.dp.fetch_data_by_url(self.url)
        self.assertIsNone(web_data)

    # def test_removeDataByWebID(self):
    #     """test the removeDataByWebID method"""
    #     self.db.updateLink(self.url, self.raw_content)

    #     # assert that data is inserted correctly in the database
    #     web_data = self.db.fetch_data_by_url(self.url)
    #     self.assertIsNotNone(web_data)

    #     # remove the inserted data
    #     self.db.removeDataByWebID(web_data['Web_ID'])

    #     # assert that data is removed from the database
    #     web_data = self.db.fetch_data_by_url(self.url)
    #     self.assertIsNone(web_data)

    def test_word_frequency_dict(self):
        """test the word_frequency_dict method"""
        words_list = ['this', 'is', 'a', 'test', 'this']
        frequency_dict = self.db.word_frequency_dict(words_list)
        self.assertEqual(frequency_dict['this'], 2)
        self.assertEqual(frequency_dict['is'], 1)
        self.assertEqual(frequency_dict['a'], 1)
        self.assertEqual(frequency_dict['test'], 1)

    def tearDown(self):
        """clean up after the test"""
        self.db.close()
        # os.remove(self.db_name)

if __name__ == '__main__':
    unittest.main()
