# Okay

import unittest
import os
from ELT_transform import main_database

class TestMainDatabase(unittest.TestCase):

    def setUp(self):
        os.remove('project/database/for_test/test.db')
        self.db = main_database('project/database/for_test/test.db')
        self.url = 'https://www.example.com'

    # test get_domain
    def test_get_domain(self):
        test_url = 'https://www.example.com'
        self.assertEqual(self.db.get_domain(test_url), 'example.com')
        self.assertNotEqual(self.db.get_domain(test_url), 'www.example.com')
    
    # test word_frequency_dict
    def test_word_frequency_dict(self):
        test_word_list = ['a', 'b', 'c', 'a', 'b', 'a']
        self.assertEqual(self.db.word_frequency_dict(test_word_list), {'a': 3, 'b': 2, 'c': 1})

    def tearDown(self):
        self.db.close()
        
if __name__ == '__main__':
    unittest.main()
