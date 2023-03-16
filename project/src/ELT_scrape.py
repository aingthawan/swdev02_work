# from rawKeeper_ELT import *  Moved in here
from singleScrape import *
from linkChecker import *
import requests

class rawKeeper:
    def __init__(self, database_file):
        self.conn = sqlite3.connect(database_file)
        self.cursor = self.conn.cursor()
        self.createTable()

    # tested
    def createTable(self):
        """Create table for raw content"""
        self.cursor.execute("CREATE TABLE IF NOT EXISTS RawMaterial(URL, raw_content)")
        self.conn.commit()

    # tested
    def insertRaw(self, url, raw_content):
        """Insert the url and raw content into the table"""
        self.cursor.execute("INSERT INTO RawMaterial VALUES (?, ?)", (url, raw_content))
        self.conn.commit()
        
    # tested
    def removeRaw(self, url):
        """Remove the url from the table"""
        self.cursor.execute("DELETE FROM RawMaterial WHERE URL = ?", (url,))
        self.conn.commit()

    # tested
    def checkRaw(self, url):
        """Check if the url already exists in the table"""
        self.cursor.execute("SELECT URL FROM RawMaterial WHERE URL = ?", (url,))
        result = self.cursor.fetchone()
        return result

    def close(self):
    # def __del__(self)
        """Close the connection"""
        self.conn.commit()
        self.conn.close()


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
    
    def checkAccessibility(url):
        """Check Whether URL is still accessible"""
        if requests.head(url).status_code == 200:
            return True
        else:
            return False

    # tested
    def crawl(self, url, current_depth, limit_depth):
        """Crawl the website and keep the raw content in the database"""
        # check if the current depth is less than the limit depth
        try:
            if current_depth <= limit_depth:
                # check if url not exists in the raw database or main database or not accessible
                if (self.rk.checkRaw(url) or self.lc.alreadyScrape(url)) or (not self.checkAccessibility(url)):
                    pass
                else:
                    # get the raw content
                    get_raw = self.ps.get_raw_html(url)
                    # check if the raw content is not empty
                    if get_raw is not None:
                        # insert the raw content into the database
                        self.rk.insertRaw(url, get_raw)
                    else:
                        pass

                    # crawl all the back links
                    for link in self.ps.scrape_all_urls(get_raw):
                        # check if the link is from the same domain and the current depth is less than the limit depth, then crawl the link
                        if (current_depth+1 <= limit_depth):
                            if (self.get_domain(link) == self.get_domain(url)):
                                print("Crawling: ", link)
                                self.crawl(link, current_depth + 1, limit_depth)
                            else:
                                print("not from the same domain")
                                pass
                        else:
                            # print("Limit depth reached")
                            pass
            else:
                pass
        # if there is an error, just pass
        except Exception as e:
            print(e)
            pass
        
    def close(self):
        self.rk.close()
        self.lc.close()    

if __name__ == "__main__":

    tinderURL = [
        "https://petapixel.com/2023/03/03/apples-29-year-old-landmark-quicktake-100-camera-falters-in-2023/",
    ]

    rawfilename = "database_elt_raw_small.db"
    mainfilename = "database_elt_main_small.db"
    db_path = "project\\database\\for_dev\\"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    start_depth = 1
    limit_depth = 2
    
    for link in (tinderURL):
    # for link in tinderURL:
        print("Crawling: ", link)
        grc.crawl(link, start_depth, limit_depth)

    print("\n\nDone\n\n")
    grc.close()





















#                                     ,-~ |
#        ________________          o==]___|
#       |                |            \ \
#       |________________|            /\ \
#  __  /  _,-----._      )           |  \ \.
# |_||/_-~         `.   /()          |  /|]_|_____
#   |//              \ |              \/ /_-~     ~-_
#   //________________||              / //___________\
#  //__|______________| \____________/ //___/-\ \~-_
# ((_________________/_-o___________/_//___/  /\,\  \
#  |__/(  ((====)o===--~~                 (  ( (o/)  )
#       \  ``==' /                         \  `--'  /
#        `-.__,-'       Vespa P-200 E       `-.__,-'
# 
# Ref : https://www.asciiart.eu/vehicles/motorcycles