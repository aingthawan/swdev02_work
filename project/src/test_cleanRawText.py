from cleanRawText import *
import unittest

class TestTextCleaner(unittest.TestCase):
    def setUp(self):
        self.tc = TextCleaners()

    def test_normalize(self):
        raw_text = "This Is a Test"
        expected_output = "this is a test"
        self.assertEqual(self.tc.normalize(raw_text), expected_output)

        raw_text = "SIVIS.PACEM-PARA/BELLUM"
        expected_output = "sivis.pacem-para/bellum"
        self.assertNotEqual(self.tc.normalize(raw_text), expected_output)
        expected_output = "sivis pacem para bellum"
        self.assertEqual(self.tc.normalize(raw_text), expected_output)

        raw_text = ""
        expected_output = ""
        self.assertEqual(self.tc.normalize(raw_text), expected_output)

    def test_remove_stopwords(self):
        raw_text = "this is a test to remove stopwords"
        expected_output = "test remove stopwords"
        self.assertEqual(self.tc.remove_stopwords(raw_text), expected_output)
        self.assertNotEqual(self.tc.remove_stopwords(raw_text), raw_text)

    def test_lemmatize(self):
        raw_text = "oh yeah oh yeah oh oh yeah"
        expected_output = ['oh', 'yeah', 'oh', 'yeah', 'oh', 'oh', 'yeah']
        self.assertEqual(self.tc.lemmatize(raw_text), expected_output)
        raw_text = "walks walked walk sleep slept"
        expected_output = ['walk', 'walk', 'walk', 'sleep', 'sleep']
        self.assertEqual(self.tc.lemmatize(raw_text), expected_output)
        
if __name__ == '__main__':
    unittest.main()
