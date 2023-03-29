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
        self.lc = LinkCheckers(main_database_file)
        self.ps = pageScrapers()

    # tested
    def get_domain(self, url):
        """Get domain name (example.com) from a url"""
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        if domain.startswith('www.'):
            domain = domain[4:]
        return domain
    
    def temp_tinder_check(self, url):
        for d in tinderURL:
            if url in d:
                return True
        return False
        
    def crawl(self, url, current_depth, limit_depth):
        """crawl the website"""
        global tinderURL
        # check if not exceed the limit
        if current_depth <= limit_depth:
            # check if url is exist in the raw and main database
            if not self.rk.checkRaw(url) and not self.lc.alreadyScrape(url):
                # OK to scrape
                get_raw = self.ps.get_raw_html(url)
                if get_raw is not None:
                    print("Level : ", current_depth," Crawling: ", url)
                    self.rk.insertRaw(url, get_raw)
                
                # get all the links from the url
                all_link = self.ps.scrape_all_urls(get_raw)
                for link in all_link:
                    # check if the link is from the same domain
                    if (self.get_domain(link) == self.get_domain(url)) and not self.temp_tinder_check(link) and (current_depth+1 <= limit_depth):
                        # add the link to the list
                        tinderURL.append({link : [current_depth+1,3]})
        return

    def close(self):
        self.rk.close()
        self.lc.close()
        return

def main():
    global tinderURL
    # initialize the class
    grc = get_raw_content("project\\database\\database_elt_raw.db", "project\\database\\database_elt_main.db")
    # grc = get_raw_content("project\\database\\for_dev\\database_elt_raw_small.db", "project\\database\\for_dev\\database_elt_main_small.db")
    while spider_alive:
        
        while spider_pause or spider_pause_signal:
            print("Spider is paused")
            time.sleep(5)
            if spider_quit:
                # dump the tinderURL to pickle
                with open("project\\pickle_temp\\spider.pkl", "wb") as f:
                    pickle.dump(tinderURL, f)
                print("Dumped the tinderURL to pickle")
                return        
        if len(tinderURL) == 0:
            time.sleep(5)
            print("No url to crawl")
        else:
            link = tinderURL.pop(0)
            print("Queue length : ", len(tinderURL))
            try:
                grc.crawl(list(link.keys())[0], list(link.values())[0][0], list(link.values())[0][1])
            except Exception as e:
                print("Error : ", e)
                pass
    return

def spider_control():
    global spider_pause
    global spider_quit
    global tinderURL
    while True:
        command = input("Enter command : ")
        if command == "pause":
            spider_pause = True
        elif command == "resume":
            spider_pause = False
        elif command == "quit":
            transform_stop()
            spider_pause = True
            spider_quit = True
            sys.exit()
        else:
            print(tinderURL)
            print("add url")
            tinderURL.append({command : [1,3]})
            print(tinderURL)
            
def spider_pauser():
    global spider_pause_signal
    print("Pausing Spider...")
    spider_pause = True

# tinderURL = [{"https://www.35mmc.com/19/03/2023/ilford-xp2-high-street-superhero-film-review-by-ted-arye/": [1,3]}, ]
tinderURL_start = []
spider_alive = True
spider_pause = False
spider_quit = False

spider_pause_signal = False

if __name__ == "__main__":
    
    print("Starting the spider")
    
    try:
        print("Loading the pickle file")
        with open("project\\pickle_temp\\spider.pkl", "rb") as f:
            tinderURL = pickle.load(f)
        print("\n\n\ntinderURL : ", len(tinderURL), " urls\n\n\n")
    except:
        print("No pickle file found, creating a new one")
        with open("project\\pickle_temp\\spider.pkl", "wb") as f:
            pickle.dump(tinderURL_start, f)
        with open("project\\pickle_temp\\spider.pkl", "rb") as f:
            tinderURL = pickle.load(f)
        print("\n\n\ntinderURL : ", tinderURL, "\n\n\n")
        
    # start the spider
    spider_thread = threading.Thread(target=main)
    spider_thread.start()
    
    transform_thread = threading.Thread(target=transform_main)
    transform_thread.start()
    
    spider_control_thread = threading.Thread(target=spider_control)
    spider_control_thread.start()
    
    spider_thread.join()
    spider_control_thread.join()
    transform_thread.join()