import unittest
from unittest.mock import MagicMock, Mock
from linkChecker import LinkCheckers


class TestLinkCheckers(unittest.TestCase):
    def setUp(self):
        #  Mock the database
        self.db = Mock()
        # Mock the cursor
        self.cursor = Mock()
        # Set the cursor to return when the database is called
        self.db.cursor.return_value = self.cursor
        self.lc = LinkCheckers(database_file=self.db)

    def test_createTable(self):
        self.lc.createTable()
        self.cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS Reference_Domain(Domain_Name, Ref_Count)")
        self.cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS web_Data(Web_ID, URL, All_Word, Ref_To)")
        self.cursor.execute.assert_any_call("CREATE TABLE IF NOT EXISTS Inverted_Index(Word, Document_Freq, Inverted_Dict)")

    
    # def test_compareDomains(self):
    #     link_checkers = LinkCheckers(database_file='dummy.db')
    #     # same domain
    #     self.assertTrue(link_checkers.compareDomains('http://example.com', 'http://www.example.com'))
    #     self.assertTrue(link_checkers.compareDomains('https://www.facebook.com/marketplace/?ref=bookmark', 'https://www.facebook.com/marketplace/item/579716220723160/?ref=browse_tab&referral_code=marketplace_general&referral_story_type=general&tracking=%7B%22qid%22%3A%22-4704314853361074380%22%2C%22mf_story_key%22%3A%2228293260324629535%22%2C%22commerce_rank_obj%22%3A%22%7B%5C%22target_id%5C%22%3A28293260324629535%2C%5C%22target_type%5C%22%3A6%2C%5C%22primary_position%5C%22%3A2%2C%5C%22ranking_signature%5C%22%3A2309614604679905280%2C%5C%22commerce_channel%5C%22%3A501%2C%5C%22value%5C%22%3A0.00044212994211911%2C%5C%22upsell_type%5C%22%3A100%2C%5C%22candidate_retrieval_source_map%5C%22%3A%7B%5C%225971502349598032%5C%22%3A3501%2C%5C%225602592346530396%5C%22%3A3501%2C%5C%225790604061047107%5C%22%3A3501%2C%5C%226396923580319915%5C%22%3A3501%2C%5C%226285125281519548%5C%22%3A3501%2C%5C%226037848016261589%5C%22%3A3501%7D%2C%5C%22grouping_info%5C%22%3Anull%7D%22%2C%22lightning_feed_qid%22%3A%22-4704315540721105245%22%2C%22lightning_feed_ranking_signature%22%3A%222309614604679905280%22%2C%22ftmd_400706%22%3A%22111112l%22%7D'))

    #     # different domains
    #     self.assertFalse(link_checkers.compareDomains('http://example.com', 'http://other.com'))

if __name__ == '__main__':
    unittest.main()
    