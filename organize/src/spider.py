from raw_manager import raw_manager
from text_processor import text_processor
import threading


class spiderman:
    """駆けろ！スパイダーマン  Yeah! Yeah! Yea~~ah!,  WOW! """
    
    def __init__(self):
        self.rm = raw_manager("organize\\src\\database\\raw.db")
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
                
                # for each link, crawl link
                for link in links:
                    self.crawl_link(link, depth + 1, limit)
        else:
            pass    

def peter_parker(starter):
    peter = spiderman()
    for url in starter:
        peter.crawl_link(url, 1, 2)
    del peter
    
if __name__ == "__main__":    
    
    starter = ["https://petapixel.com/2023/03/03/apples-29-year-old-landmark-quicktake-100-camera-falters-in-2023/",]
    
    threading.Thread(target=peter_parker(starter)).start()
    
    print("Spiderman is on the job!")