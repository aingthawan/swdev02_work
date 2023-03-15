from raw_manager import raw_manager
from text_processor import text_processor
import threading
import time
import os
import sys

class spiderman:
    """駆けろ！スパイダーマン  Yeah! Yeah! Yea~~ah!,  WOW! """
    
    def __init__(self):
        self.rm = raw_manager("organize\\database\\raw.db")
        self.tp = text_processor()
    
    def __del__(self):
        del self.rm

    def insert_new_raw(self, url, raw_text):
        self.rm.insert_new(url, raw_text)

    def crawl_link(self, url, depth, limit):
        # check if depth is less than limit
        if depth <= limit:
            while paused:
                os.system("cls")
                print("Spiderman is paused")
                time.sleep(2)
                
            if self.tp.url_accessibility_check(url) and not self.rm.url_exist_check(url):
                print(url)
                # get raw text from url
                raw_text = self.tp.get_raw_html(url)
                
                # self.insert_new_raw(url, raw_text)
                # separate thread for inserting new raw content
                threading.Thread(target=self.insert_new_raw(url, raw_text)).start()
                
                # get all links from url
                links = self.tp.scrape_all_urls(raw_text)
                
                # for each link, crawl link
                for link in links:
                    self.crawl_link(link, depth + 1, limit)
            else:
                pass
        else:
            pass    

def peter_parker():
    starter = ["https://petapixel.com/2023/03/03/apples-29-year-old-landmark-quicktake-100-camera-falters-in-2023/",]
    peter = spiderman()
    for url in starter:
        peter.crawl_link(url, 1, 2)
    del peter
    
def job_controller():
    global paused
    while True:
        command = input("\nGet command: \n")
        if command == "p":
            paused = True
            print("\npaused\n")
            time.sleep(5)  # sleep for 5 seconds to get new command
        elif command == "c":
            paused = False
            print("\ncontinued\n")
        elif command == "q": # quit
            print("\nquitting\n")
            # pause the spiderman
            paused = True
            # sys.exit()
        else:
            print("\ninvalid command\n")

paused = False # Global variable for pausing

if __name__ == "__main__":    
    # separate thread for peter_parker then continue
    
    threading.Thread(target=peter_parker).start()
    
    print("Spiderman is on the job!")
    
    threading.Thread(target=job_controller).start()