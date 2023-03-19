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
    
    
    def crawl(self, url, current_depth, limit_depth):
        """Crawl the website and keep the raw content in the database"""
        # check if the current depth is less than the limit depth
        global tinderURL
        global spider_status
        try:
            while spider_pause:
                print("Spider is paused")
                time.sleep(1)
                spider_status = True
                if spider_quitting: # if spider is quitting, dump the list into the pickle file
                    print("Spider is quitting")
                    with open("project\\pickle_temp\\spider.pkl", 'wb') as f:
                        print("Dumping the list ( " ,len(tinderURL), " urls ) into the pickle file")
                        pickle.dump(tinderURL, f)
                    return sys.exit()
            spider_status = False
            
            for i in tinderURL:
                if url in i:
                    tinderURL.remove(i)
                    
            if current_depth <= limit_depth:
                if not self.rk.checkRaw(url) and not self.lc.alreadyScrape(url):
                    get_raw = self.ps.get_raw_html(url)
                    if get_raw is not None:
                        print("Level : ", current_depth," Crawling: ", url)
                        self.rk.insertRaw(url, get_raw)
                        
                    all_link = self.ps.scrape_all_urls(get_raw)
                    if current_depth+1 <= limit_depth:
                        for link in all_link:
                            tinderURL.append({link:[current_depth+1, limit_depth]})
                        print("All url in queue : ", len(tinderURL))
                        
                    for link in all_link:
                        if (current_depth+1 <= limit_depth):
                            if (self.get_domain(link) == self.get_domain(url)):
                                self.crawl(link, current_depth + 1, limit_depth)
                            else:
                                print("not from the same domain")
                        else:
                            return
            else:
                return
        except Exception as e:
            print(e)
            pass
        spider_status = True
        return
    
    def close(self):
        self.rk.close()
        self.lc.close()    



def spider_job():
    global spider_status
    db_path = "project\\database\\for_dev\\"
    rawfilename = "database_elt_raw_small.db"
    mainfilename = "database_elt_main_small.db"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    while spider_quitting == False:
        if len(tinderURL) != 0:
            for link in tinderURL:
            # format [ {'url1':[current_depth,limit_depth] }, {'url2':[current_depth,limit_depth] } ]
                print("Crawling: ", link)
                grc.crawl(list(link.keys())[0], list(link.values())[0][0], list(link.values())[0][1])
        else:
            print("No more url to crawl")
            time.sleep(1)
    sys.exit()
        

    # print("\n\nDone\n\n")
    # spider_status = True
    # grc.close()
    # return

def spider_pauser():
    global spider_pause
    spider_pause = True
    print("\n\n\nSpider Pause Signal Received\n")

def spider_poker():
    global spider_pause
    spider_pause = False
    print("\n\n\nSpider Poke Signal Received\n")
    
def spider_stopper():
    global spider_quitting
    global spider_pause
    spider_pause = True
    spider_quitting = True
    transform_stop()
    print("\n\n\nSpider Stop Signal Received\n")

def spider_job_control():
    global spider_pause
    global spider_quitting
    global spider_status
    global tinderURL
    
    global transform_status
    global transform_pause
    global transform_quit
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
            transform_stop()
            sys.exit()
        else:
            print("Invalid command")
            
            
            
spider_pause = False
spider_quitting = False
spider_status = False # False is crawling, True is chilling
# tinderURL = [{"https://www.dpreview.com/news/9657627837/leica-announces-vario-elmar-sl-100-400-f5-6-3-and-1-4x-extender": [1, 3],},]
tinderURL = []
            
# if __name__ == "__main__":
def ELT_scrape_main():
    global tinderURL
    global spider_status
    try:
        print("Loading the pickle file")
        with open("project\\pickle_temp\\spider.pkl", "rb") as f:
            tinderURL = pickle.load(f)
        print("\n\n\ntinderURL : ", tinderURL, "\n\n\n")
    except:
        print("No pickle file found, creating a new one")
        with open("project\\pickle_temp\\spider.pkl", "wb") as f:
            pickle.dump(tinderURL, f)
        with open("project\\pickle_temp\\spider.pkl", "rb") as f:
            tinderURL = pickle.load(f)
        print("\n\n\ntinderURL : ", tinderURL, "\n\n\n")
    
    transform_job = threading.Thread(target=transform_start)
    transform_job.start()
    # human control
    # job_cont_thread = threading.Thread(target=spider_job_control)
    # job_cont_thread.start()
    # start the spider
    spider_thread = threading.Thread(target=spider_job)
    spider_status = True
    spider_thread.start()
    
    transform_job.join()
    # job_cont_thread.join()
    spider_thread.join()
    