from raw_manager import raw_manager
from text_processor import text_processor
import threading
import time
import os
import sys
import pickle

class spiderman:
    """駆けろ！スパイダーマン  Yeah! Yeah! Yea~~ah!,  WOW! """
    
    def __init__(self):
        global starter
        self.rm = raw_manager("organize\\src\\database\\raw_test.db")
        self.tp = text_processor()
    
    def __del__(self):
        del self.rm

    def insert_new_raw(self, url, raw_text):
        self.rm.insert_new(url, raw_text)

    def crawl_link(self, url, depth, limit):
        # check if depth is less than limit
        if depth <= limit:
                
            if self.tp.url_accessibility_check(url) and not self.rm.url_exist_check(url):
                print(url)
                # get raw text from url
                raw_text = self.tp.get_raw_html(url)
                
                # self.insert_new_raw(url, raw_text)
                # separate thread for inserting new raw content
                threading.Thread(target=self.insert_new_raw(url, raw_text)).start()
                
                # get all links from url
                links = self.tp.scrape_all_urls(raw_text)
                
                # check if url in starter
                if url in starter:
                    starter.remove(url)
                # append links to starter, if not exceed limit in next depth
                if depth + 1 <= limit:
                    starter.extend(links)
                
                while paused:
                    os.system("cls")
                    print("Spiderman is paused")
                    time.sleep(2)
                    if quitting:
                        # save the variables to a file
                        with open(path+pickle_file, 'wb') as f:
                            print("saving variable state : starter")
                            pickle.dump(starter, f)
                        # quit program
                        print("quitting program")
                        sys.exit()
                
                # for each link, crawl link
                for link in links:
                    # check if link having same domain a url and not a picture
                    if self.tp.domain_check(url, link) and not self.tp.picture_check(link):
                        self.crawl_link(link, depth + 1, limit)
                    else:
                        pass
            else:
                pass
        else:
            return 

def job_controller():
    global paused
    global quitting
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
            quitting = True
            sys.exit()
        else:
            print("\ninvalid command\n")

def peter_parker():
    peter = spiderman()
    for url in starter:
        peter.crawl_link(url, 1, 2)
    print("Spiderman is done!")
    del peter
    return sys.exit()
    

starter = [ # "https://petapixel.com/2023/03/03/apples-29-year-old-landmark-quicktake-100-camera-falters-in-2023/",
           "https://www.35mmc.com/14/03/2023/5-frames-in-nottingham-with-a-yashica-fx-d-and-contax-zeiss-85mm-f1-4-by-ellis-thomas/",
        #    "https://fstoppers.com/reviews/review-new-fujifilm-instax-mini-12-camera-627478"
           ]
paused = False # Global variable for pausing
quitting = False # Global variable for quitting

path = "organize\\src\\pickle_state\\"
pickle_file = "test_spider_state.pkl"

if __name__ == "__main__":    
    
    try:
        # Load the variables from the file
        with open(path+pickle_file, 'rb') as f:
            starter = pickle.load(f)
    except:
        with open(path+pickle_file, 'wb') as f:
            pickle.dump(starter, f)
        with open(path+pickle_file, 'rb') as f:
            starter = pickle.load(f)
    
    # separate thread for peter_parker then continue
    threading.Thread(target=peter_parker).start()
    
    print("Spiderman is on the job!")
    
    threading.Thread(target=job_controller).start()
    