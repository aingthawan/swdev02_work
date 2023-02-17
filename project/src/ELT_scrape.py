from rawKeeper_ELT import *
from singleScrape import *
from linkChecker import *
import tqdm


class get_raw_content:
    def __init__(self, raw_database_file, main_database_file):
        self.rk = rawKeeper(raw_database_file)
        self.ps = pageScrapers()

        self.lc = LinkCheckers(main_database_file)

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
        try:
            if current_depth <= limit_depth:
                # check if url not exists in the raw database or main database
                if self.rk.checkRaw(url) or self.lc.alreadyScrape(url):
                    # print("Already exists in the database")
                    pass
                else:
                    # print("Crawling: ", url)
                    # get the raw content
                    get_raw = self.ps.get_raw_html(url)
                    # check if the raw content is not empty
                    if get_raw is not None:
                        # get all the links in the page
                        # all_links = self.ps.scrape_all_urls(get_raw)
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
                            print("Limit depth reached")
                            pass
            else:
                pass
        # if there is an error, just pass
        except Exception as e:
            print(e)
            pass


    # def crawl_debug(self, url, current_depth, limit_depth):
    #     if current_depth <= limit_depth:
    #         if self.rk.checkRaw(url) or self.lc.alreadyScrape(url):
    #             print("Already exists in the database")
    #             pass
    #         else:
    #             print("Crawling: ", url)
    #             get_raw = self.ps.get_raw_html(url)
    #             print("Raw content: ", get_raw[:100])
    #             if get_raw is not None:
    #                 print("Content OK")
    #                 print("Valid Child links: ")
    #                 all_links = self.ps.scrape_all_urls(get_raw)
    #                 for link in all_links:
    #                     if self.get_domain(link) == self.get_domain(url):
    #                         print(link)
    #             else:
    #                 pass
    #     else:
    #         print("Limit depth reached")
    #         pass


    

if __name__ == "__main__":

    tinderURL = {
        # "https://photographylife.com/reviews/fuji-x100f",
        # "https://www.dpreview.com/reviews/sony-a7rv-review?utm_source=self-desktop&utm_medium=marquee&utm_campaign=traffic_source",
        # "https://www.35mmc.com/02/02/2023/hedeco-lime-two-low-profile-shoe-mount-light-meter-review/",
        # "https://petapixel.com/2023/02/03/canon-usa-settles-with-employees-affected-by-2020-ransomware-attack/",
        # "https://www.35mmc.com/14/10/2021/pentax-iqzoom-928-review/",
        # "https://www.photographyblog.com/reviews/om_system_om_5_review",
        # "https://www.outdoorphotographer.com/on-location/featured-stories/",
        # "https://www.peerspace.com/resources/category/photography/"
        # "https://www.outdoorphotographer.com/on-location/travel/"
        # "https://petapixel.com/topic/reviews/",
        # "https://petapixel.com/2022/11/23/zhiyuns-fiveray-m40-pocket-light-and-f100-light-stick-are-super-bright/",
        "https://petapixel.com/2023/02/16/haunting-footage-of-titanic-shipwreck-released-for-the-first-time/",
    }

    rawfilename = "database_elt_raw_backup4.db"
    mainfilename = "database_elt_main2.db"
    db_path = "project\database\\"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    start_depth = 1
    limit_depth = 4

    for link in (tinderURL):
    # for link in tinderURL:
        print("Crawling: ", link)
        grc.crawl(link, start_depth, limit_depth)

    print("\n\nDone\n\n")





















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