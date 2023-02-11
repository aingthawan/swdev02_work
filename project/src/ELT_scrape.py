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
        print("at : ", url)
        if current_depth <= limit_depth:
            # check if url not exists in the raw database
            if self.rk.checkRaw(url):
                # print("Already exists in the database")
                pass
            else:
                # get the raw content
                get_raw = self.ps.get_raw_html(url)
                # check if the raw content is not empty
                if get_raw is not None:
                    # get all the links in the page
                    all_links = self.ps.scrape_all_urls(get_raw.text)
                    # insert the raw content into the database
                    self.rk.insertRaw(url, get_raw.text)
                else:
                    pass

                # crawl the links
                for link in all_links:
                    # check if the link is from the same domain
                    if self.get_domain(link) == self.get_domain(url):
                        self.crawl(link, current_depth + 1, limit_depth)
                    else:
                        pass
        else:
            # print("Limit depth reached")
            pass

    

if __name__ == "__main__":

    tinderURL = {
        # "https://photographylife.com/reviews/fuji-x100f",
        # "https://www.dpreview.com/reviews/sony-a7rv-review?utm_source=self-desktop&utm_medium=marquee&utm_campaign=traffic_source",
        "https://www.35mmc.com/02/02/2023/hedeco-lime-two-low-profile-shoe-mount-light-meter-review/",
        # "https://petapixel.com/2023/02/03/canon-usa-settles-with-employees-affected-by-2020-ransomware-attack/",
        # "https://www.35mmc.com/14/10/2021/pentax-iqzoom-928-review/"
    }

    rawfilename = "database_elt_raw2.db"
    mainfilename = "database_elt_main2.db"
    db_path = "project\database\\"

    grc = get_raw_content(db_path+rawfilename, db_path+mainfilename)
    start_depth = 1
    limit_depth = 7

    for link in tqdm.tqdm(tinderURL):
        grc.crawl(link, start_depth, limit_depth)

    print("\n\nDone\n\n")
