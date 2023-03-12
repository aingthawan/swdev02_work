import unittest
from unittest.mock import patch
from linkChecker import LinkCheckers


class TestMyClass(unittest.TestCase):

    def setUp(self):
        self.my_class = LinkCheckers('project/database/for_test/test_linkChecker_database.db')

    @patch('linkChecker.requests.get')
    def test_checkAccessibility_success(self, mock_get):
        # Mock a successful HTTP GET request
        mock_get.return_value.ok = True
        url = "http://www.google.com"
        self.assertTrue(self.my_class.checkAccessibility(url))
        mock_get.assert_called_once_with(url)

    @patch('linkChecker.requests.get')
    def test_checkAccessibility_failure(self, mock_get):
        # Mock a failed HTTP GET request
        mock_get.return_value.ok = False
        url = "http://www.thisisnotavalidurl.com"
        self.assertFalse(self.my_class.checkAccessibility(url))
        mock_get.assert_called_once_with(url)

if __name__ == '__main__':
    unittest.main()
