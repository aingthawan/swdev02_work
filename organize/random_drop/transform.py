# a file to transform the raw data into the main database
# standby and check for new data in the raw database every 5 seconds
# if new data is found, transform it and add it to the main database
# then delete the row from the raw database
# 
# Dev : AingKK.

from linkChecker import *
from dataPipeline import *
from cleanRawText import *
from singleScrape import *

from urllib.parse import urlparse
import sqlite3
import time


# def word_frequency_dict(words_list):
#     """Turn list of words into dictionary with word as key and frequency as value"""
#     frequency_dict = {}
#     for word in words_list:
#         if word in frequency_dict:
#             frequency_dict[word] += 1
#         else:
#             frequency_dict[word] = 1
#     return frequency_dict    

class raw_database:
    """class for getting the raw content from the database and remove"""
    # To use this class, you need to already have a database with a table called rawMaterial
    def __init__(self, database):
        """initialize the database"""
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()
        
    # tested
    def get_row(self): 
        """get the row from the database"""
        self.cur.execute("SELECT * FROM rawMaterial LIMIT 1")
        row = self.cur.fetchone()
        
        if row is None:
            return None
        else:
            return row

    # tested
    def delete_row(self, url):
        """delete the row from the database"""
        # try if row exist
        try:
            self.cur.execute("DELETE FROM rawMaterial WHERE url = ?", (url,))
            self.conn.commit()
        # except if row does not exist
        except:
            pass

    def close(self):
        """close the connection"""
        self.conn.commit()
        self.conn.close()
        

class main_database:
    """class for processing the raw content and insert into the database"""

    def __init__(self, main_database):
        """initialize the database"""
        self.tc = TextCleaners()
        self.ps = pageScrapers()
        self.dp = dataPipelines(main_database)

    # tested
    def get_domain(self, url):
        """Get domain name (example.com) from a url"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    # tested in datapipeline
    def updateLink(self, url, raw_content):
        """update the link into the database"""
        # check if the url is already in the database
        if self.dp.fetch_data_by_url(url) is None:
            # Clean raw content
            clean_content = self.tc.clean_raw(raw_content)
            clean_content_dict = self.word_frequency_dict(clean_content)
            
            all_backlink_list = self.ps.scrape_all_urls(raw_content)
            
            url_domain = self.get_domain(url)
            # get a list of unique domain from all backlinks
            all_backlink_domain_list = []
            for link in all_backlink_list:
                link_domain = self.get_domain(link)
                if (self.get_domain(link) not in all_backlink_domain_list) and (link_domain != url_domain):
                    all_backlink_domain_list.append(link_domain)
            
            new_id = self.dp.getUniqueID()
        
            # updating reference domain
            self.dp.updateReferenceDomain(all_backlink_domain_list)
            # update webData
            # def updateWebData(self, web_id, url, all_words, ref_to):
            self.dp.updateWebData(new_id, url, clean_content_dict, all_backlink_domain_list)
            # update invertedIndex
            self.dp.updateInvertedIndexing(new_id, clean_content)
            # remove cache
            self.dp.removeTermInCache(list(clean_content_dict.keys()))
        else:
            print("URL : ", url, " already in database")
    
    # tested in datapipeline
    def direct_update_link(self, url):
        """update the link into the database, without raw content, using method above"""
        # get raw content of the url
        print("Updating URL : ", url)
        page_content = self.ps.get_raw_html(url)
        self.updateLink(url, page_content)

    # tested in datapipeline
    def removeData(self, url):
        """remove the data from the database"""
        temp_datarow = self.dp.fetch_data_by_url(url)
        self.dp.removeWebData(temp_datarow['URL'])
        self.dp.uncountRef(temp_datarow['Ref_To'])
        self.dp.removeInvertedIndex(temp_datarow['Web_ID'], temp_datarow['All_Word'])
        # remove cache
        self.dp.removeTermInCache(temp_datarow['All_Word'])
    
    # tested in datapipeline
    def removeDataByWebID(self, web_id):
        """remove the data from the database"""
        temp_datarow = self.dp.fetch_data_by_id(web_id)
        # if data is not None
        if temp_datarow is not None:
            self.dp.removeWebData(temp_datarow['URL'])
            self.dp.uncountRef(temp_datarow['Ref_To'])
            self.dp.removeInvertedIndex(temp_datarow['Web_ID'], temp_datarow['All_Word'])
        else:
            # print("Data with ID : ", web_id  ," not found in database")
            pass

    # tested
    def word_frequency_dict(self, words_list):
        """Turn list of words into dictionary with word as key and frequency as value"""
        frequency_dict = {}
        for word in words_list:
            if word in frequency_dict:
                frequency_dict[word] += 1
            else:
                frequency_dict[word] = 1
        return frequency_dict
    
    def close(self):
        """close the connection"""
        self.dp.close()
    

def data_processing():
    
    directory = "project\database\\for_dev\\"
    raw_dir = directory + "database_elt_raw_small.db"
    main_dir = directory + "database_elt_main_small.db"
    
    rawd = raw_database(raw_dir)
    
    try:
        while True:
            
            row_temp = rawd.get_row()
            
            if row_temp is None:
                print("Table is empty. Waiting for data...")
                time.sleep(5)
                continue

            else:
                mdb = main_database(main_dir)
                print("Processing data...")
                start_time = time.time()
                url = row_temp[0]
                raw = row_temp[1]
                mdb.updateLink(url, raw)
                mdb.close()
                rawd.delete_row(url)
                rawd.close()
                print("Data processed. Time taken: %s seconds" % (time.time() - start_time))
    # if there is any error, remove the top row from raw database then continue
    except Exception as e:
        print(e)
        print("Error occured. Removing data from raw database...")
        rawd.delete_row(url)
        rawd.close()
        print("Data removed. Continuing...")
        data_processing()
    # if keyboard interrupt, close the connection 
    except KeyboardInterrupt:
        print("closing connection")
        try:
            mdb.close()
        except:
            pass
        rawd.close()
        exit()

        
        
if __name__ == "__main__":    
    try:
        data_processing()
    except KeyboardInterrupt:
        print("Exiting program")


#  _._     _,-'""`-._
# (,-.`._,'(       |\`-/|
#     `-.-' \ )-`( , o o)  < Katze is cat in German
#           `-    \`_`"'-        