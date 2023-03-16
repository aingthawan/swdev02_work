from rawKeeper_ELT import *
from singleScrape import *
from linkChecker import *



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
        # "https://photographylife.com/integrating-jpegmini-pro-to-lightroom-workflow",
        # "https://placesjournal.org/article/orphan-wells-oil-infrastructure-in-louisiana/",
        # "https://expertphotography.com/best-retro-camera/",
        # "https://www.newscientist.com/article/mg25634130-200-a-gift-from-nature-geothermal-energy-in-tuscanys-valle-del-diavolo/",
        # "https://www.wired.com/gallery/best-photo-video-accessories-for-iphone-android/",
        # "https://www.dpreview.com/news/7860893940/film-friday-meet-luminar-100-a-new-35mm-color-film-stock-made-kodak-aerocolor-iv-aerial-film",
        "https://fstoppers.com/film/most-overrated-and-underrated-film-cameras-2021-563868",
        "https://www.dpreview.com/articles/9885954923/canon-eos-r8-hands-on",
        # "https://www.studiobinder.com/blog/how-to-shoot-film-photography/",
        # "https://iso.500px.com/how-to-increase-your-prices-as-a-freelance-photographer/"
    }

    rawfilename = "database_elt_raw_small.db"
    mainfilename = "database_elt_main_small.db"
    db_path = "project\\database\\for_dev\\"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    start_depth = 1
    limit_depth = 3

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