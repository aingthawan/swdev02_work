from linkChecker import *
from dataPipeline import *
from cleanRawText import *
from singleScrape import *

import sqlite3
from urllib.parse import urlparse

directory = "project\src\database\\"
raw_database = directory + "database_elt_raw_test3.db"
main_database = directory + "database_elt_test1.db"


# ================================================================================================
# ================================================================================================

def word_frequency_dict(words_list):
    """Turn list of words into dictionary with word as key and frequency as value"""
    frequency_dict = {}
    for word in words_list:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return frequency_dict    

# ================================================================================================
# ================================================================================================

class raw_database:
    """class for getting the raw content from the database and remove"""

    def __init__(self, database):
        """initialize the database"""
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def get_row(self):
        """get the row from the database"""
        self.cur.execute("SELECT * FROM rawMaterial LIMIT 1")
        row = self.cur.fetchone()
        
        if row is None:
            return None
        else:
            return row

    def delete_row(self, url):
        """delete the row from the database"""
        self.cur.execute("DELETE FROM rawMaterial WHERE url = ?", (url,))
        self.conn.commit()

    def close(self):
        """close the connection"""
        self.conn.commit()
        self.conn.close()



class main_databse:
    """class for processing the raw content and insert into the database"""

    def __init__(self, main_database):
        """initialize the database"""
        self.conn = sqlite3.connect(main_database)
        self.cur = self.conn.cursor()

        self.tc = TextCleaners()
        self.ps = pageScrapers()
        self.dp = dataPipelines(main_database)

    def get_domain(self, url):
        """Get domain name (example.com) from a url"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    def updateLink(self, url, raw_content):
        """update the link into the database"""
        # Clean raw content
        clean_content = self.tc.clean(raw_content)
        all_backlink_list = self.ps.scrape_all_urls(clean_content)
        # get a list of unique domain from all backlinks
        all_backlink_domain_list = []
        for link in all_backlink_list:
            if self.get_domain(link) not in all_backlink_domain_list:
                all_backlink_domain_list.append(self.get_domain(link))
        
        new_id = self.dp.getUniqueID()

        # updating reference domain
        self.dp.updateReferenceDomain(all_backlink_domain_list)
        # update webData
        self.dp.updateWebData(new_id, url, clean_content)
        # update invertedIndex
        self.dp.updateInvertedIndex(new_id, clean_content)


    def removeData(self, url):
        """remove the data from the database"""
        temp_datarow = self.dp.fetch_data_by_url(url)
        self.dp.removeWebData(temp_datarow['URL'])
        self.dp.uncountRef(temp_datarow['Ref_To'])
        self.dp.removeInvertedIndex(temp_datarow['Web_ID'], temp_datarow['All_Word'])
