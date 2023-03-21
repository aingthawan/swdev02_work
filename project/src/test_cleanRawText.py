# Unit tests for cleanRawText.py
# Okay 

from cleanRawText import *
import unittest

class TestTextCleaner(unittest.TestCase):
    def setUp(self):
        self.tc = TextCleaners()

    def test_normalize(self):
        """test the normalize function"""
        # test normalize upper case + lower case
        raw_text = "This Is a Test"
        expected_output = "this is a test"
        self.assertEqual(self.tc.normalize(raw_text), expected_output)
        # test upper case + symbol
        raw_text = "SIVIS.PACEM-PARA/BELLUM"
        expected_output = "sivis.pacem-para/bellum"
        # assertNotEqual
        self.assertNotEqual(self.tc.normalize(raw_text), expected_output)
        expected_output = "sivis pacem para bellum"
        # assertEqual
        self.assertEqual(self.tc.normalize(raw_text), expected_output)
        # test empty string
        raw_text = ""
        expected_output = ""
        self.assertEqual(self.tc.normalize(raw_text), expected_output)

    def test_remove_stopwords(self):
        """test the remove_stopwords function"""
        raw_text = "this is a test to remove stopwords"
        expected_output = "test remove stopwords"
        self.assertEqual(self.tc.remove_stopwords(raw_text), expected_output)
        self.assertNotEqual(self.tc.remove_stopwords(raw_text), raw_text)

    def test_lemmatize(self):
        """test the lemmatize function"""
        raw_text = "oh yeah oh yeah oh oh yeah"
        expected_output = ['oh', 'yeah', 'oh', 'yeah', 'oh', 'oh', 'yeah']
        self.assertEqual(self.tc.lemmatize(raw_text), expected_output)
        raw_text = "walks walked walk sleep slept"
        expected_output = ['walk', 'walk', 'walk', 'sleep', 'sleep']
        self.assertEqual(self.tc.lemmatize(raw_text), expected_output)
        
    def test_clean(self):
        """test the clean function"""
        # for clean user input
        self.assertEqual(self.tc.clean("The quick brown fox jumps over the lazy dog"), ["quick", "brown", "fox", "jump", "lazy", "dog"])
        
        # Test with punctuation and numbers
        self.assertEqual(self.tc.clean("Hello, World! 123"), ["hello", "world", "123"])
        
    def test_clean_raw(self):
        """test the clean_raw function"""
        # for clean raw text
        raw_text = "<html><body><p>Hello, World!</p></body></html>"
        self.assertEqual(self.tc.clean_raw(raw_text), ["hello", "world"])
        
        # Test with nested HTML tags
        raw_text = "<html><body><div><p>Hello, World!</p></div></body></html>"
        self.assertEqual(self.tc.clean_raw(raw_text), ["hello", "world"])
        
        # Test with XML input
        raw_text = "<root><p>Hello, World!</p></root>"
        self.assertEqual(self.tc.clean_raw(raw_text), ["hello", "world"])

if __name__ == '__main__':
    unittest.main()