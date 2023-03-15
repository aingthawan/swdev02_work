from raw_manager import raw_manager
from main_manager import main_manager
from text_processor import text_processor

class data_transform:

    def __init__(self, main_db, raw_db):
        self.rm = raw_manager(raw_db)
        self.tp = text_processor()
        self.mm = main_manager(main_db)

    def __del__(self):
        del self.rm
        del self.mm
        del self.tp

    def update_web(self, url, raw_html):
        # check if url exist in the table
        if not self.rm.url_exist_check(url):
            all_word_list = self.tp.clean_raw(raw_html)
            all_url_list = self.tp.scrape_all_urls(raw_html)
            all_ref_domain_list = self.tp.get_ref_domain(url, all_url_list)
            # things to update
            new_id = self.mm.get_new_id()
            self.mm.update_web_data(new_id, url, all_word_list, all_ref_domain_list)
            self.mm.update_reference_domain(all_ref_domain_list)
            self.mm.update_inverted_index(new_id, all_word_list)
            return
        else:
            print("data_transform : URL already exist in the raw database")
            return

    def direct_update_web(self, url):
        """Input a single url, update the main database directly"""
        if self.tp.url_accessibility_check(url):
            raw_html = self.tp.get_raw_html(url)
            self.update_web(url, raw_html)
            return
        else:
            print("data_transform : URL is not accessible")
            return    