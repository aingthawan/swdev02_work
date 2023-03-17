from rawKeeper_ELT import *
from singleScrape import *
from linkChecker import *
from ELT_transform import *
import pickle
import time
import sys
import threading


class get_raw_content:
    def __init__(self, raw_database_file, main_database_file):
        self.rk = rawKeeper(raw_database_file)
        self.ps = pageScrapers()

        self.lc = LinkCheckers(main_database_file)

    # tested
    def get_domain(self, url):
        """Get domain name (example.com) from a url"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain

    # tested
    def crawl(self, url, current_depth, limit_depth):
        """Crawl the website and keep the raw content in the database"""
        # check if the current depth is less than the limit depth
        global tinderURL
        try:
            # Quitting Script ============================
            while spider_pause:
                print("Spider is paused")
                time.sleep(1)
                if spider_quitting:
                    print("Spider is quitting")
                    # dump the list into the pickle file
                    print("Dumping the list into the pickle file")
                    with open('tinderURL.pickle', 'wb') as f:
                        pickle.dump(tinderURL, f)
                    sys.exit()                    
            # ============================================
            if url in tinderURL:
                # remove the url from the list
                tinderURL.remove(url)
            if current_depth <= limit_depth:
                # check if url not exists in the raw database or main database
                if self.rk.checkRaw(url) or self.lc.alreadyScrape(url):
                    pass
                else:
                    # get the raw content
                    get_raw = self.ps.get_raw_html(url)
                    
                    # check if the raw content is not empty
                    if get_raw is not None:
                        # get all the links in the page
                        # insert the raw content into the database
                        self.rk.insertRaw(url, get_raw)
                        
                    else:
                        pass

                    # crawl all the back links
                    all_link = self.ps.scrape_all_urls(get_raw)
                    # put the link into the list tinderURL
                    tinderURL.extend(all_link)
                    for link in all_link:
                        # check if the link is from the same domain and the current depth is less than the limit depth, then crawl the link
                        if (current_depth+1 <= limit_depth):
                            if (self.get_domain(link) == self.get_domain(url)):
                                print("Crawling: ", link)
                                self.crawl(link, current_depth + 1, limit_depth)
                            else:
                                print("not from the same domain")
                                pass
                        else:
                            # end layer
                            return
            else:
                return
        # if there is an error, just pass
        except Exception as e:
            print(e)
            pass
        return
    
    def close(self):
        self.rk.close()
        self.lc.close()    

def spider_job():
    db_path = "project\\database\\for_dev\\"
    rawfilename = "database_elt_raw_small.db"
    mainfilename = "database_elt_main_small.db"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    start_depth = 1
    limit_depth = 3

    for link in (tinderURL):
    # for link in tinderURL:
        print("Crawling: ", link)
        grc.crawl(link, start_depth, limit_depth)

    print("\n\nDone\n\n")
    
    grc.close()


spider_pause = False
spider_quitting = False
spider_status = False # False is not finished, True is finished
tinderURL = [
        "https://www.dpreview.com/articles/9885954923/canon-eos-r8-hands-on",
    ]

def spider():
    global tinderURL
    try:
        with open("project\\pickle_temp\\spider.pickle", "rb") as f:
            tinderURL = pickle.load(f)
    except:
        with open("project\\pickle_temp\\spider.pickle", "wb") as f:
            pickle.dump(tinderURL, f)
        with open("project\\pickle_temp\\spider.pickle", "rb") as f:
            tinderURL = pickle.load(f)
    
    spider_job()

def spider_job_control():
    global spider_pause
    global spider_quitting
    global spider_status
    global tinderURL
    
    global transform_pause
    global transform_quitting
    while True:
        spider_command = input("Enter Spider command: ")
        if spider_command == "pause":
            print("Spider paused")
            spider_pause = True
        elif spider_command == "resume":
            print("Spider resumed")
            spider_pause = False
        elif spider_command == "quit":
            print("Spider quitting")
            spider_pause = True
            spider_quitting = True
            transform_pause = True
            transform_quitting = True
        else:
            print("Invalid command")
            
if __name__ == "__main__":
    transform_job = threading.Thread(target=transform_start)
    transform_job.start()
    
    job_cont_thread = threading.Thread(target=spider_job_control)
    job_cont_thread.start()
    
    spider_thread = threading.Thread(target=spider)
    spider_thread.start()
    
    print("Spider finished")