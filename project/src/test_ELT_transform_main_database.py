from ELT_transform import main_database
import unittest
from unittest.mock import patch
import tempfile
import os

class TestMainDatabase(unittest.TestCase):

    def setUp(self):
        self.db_file = tempfile.NamedTemporaryFile(delete=False)
        self.db_name = self.db_file.name
        self.db = main_database(self.db_name)

    def tearDown(self):
        self.db.dp.conn.close()
        os.unlink(self.db_name)

    @patch.object(main_database, 'get_domain')
    @patch.object(main_database, 'word_frequency_dict')
    @patch.object(main_database, 'ps')
    @patch.object(main_database, 'dp')
    def test_updateLink(self, mock_dp, mock_ps, mock_word_frequency_dict, mock_get_domain):
        mock_get_domain.return_value = 'example.com'
        mock_word_frequency_dict.return_value = {'some': 1, 'words': 2}
        mock_ps.scrape_all_urls.return_value = ['https://example.com', 'https://example.org']
        mock_dp.getUniqueID.return_value = 1
        url = 'https://example.com'
        raw_content = 'Some raw content'

        self.db.updateLink(url, raw_content)

        mock_dp.updateReferenceDomain.assert_called_with(['example.org'])
        mock_dp.updateWebData.assert_called_with(1, url, {'some': 1, 'words': 2}, ['example.org'])
        mock_dp.updateInvertedIndexing.assert_called_with(1, 'Some raw content')

    @patch.object(main_database, 'dp')
    def test_removeData(self, mock_dp):
        url = 'https://example.com'
        mock_dp.fetch_data_by_url.return_value = {'URL': url, 'Ref_To': 'example.org', 'Web_ID': 1, 'All_Word': 'Some raw content'}

        self.db.removeData(url)

        mock_dp.removeWebData.assert_called_with(url)
        mock_dp.uncountRef.assert_called_with('example.org')
        mock_dp.removeInvertedIndex.assert_called_with(1, 'Some raw content')

if __name__ == '__main__':
    unittest.main()
