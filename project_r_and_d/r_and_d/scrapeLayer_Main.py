from cleanRawText import *
from dataPipeline import *
from linkChecker import *
from singleScrape import *

from urllib.parse import urlparse

def get_domain(url):
    """Get domain name (example.com) from a url"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def word_frequency_dict(words_list):
    """Turn list of words into dictionary with word as key and frequency as value"""
    frequency_dict = {}
    for word in words_list:
        if word in frequency_dict:
            frequency_dict[word] += 1
        else:
            frequency_dict[word] = 1
    return frequency_dict


def updateLink(url):
    # newid = dataPipeline.getUniqueID()
    raw_mat = pageScraper.scrape_page(url)
    
    all_backlinks = raw_mat["backlinks"]

    page_domain = get_domain(url)

    all_domain = [] # <<<<<<<<< All domain
    all_backlink = [] # <<<<<<<<< All link founded

    for link in all_backlinks:
        # get domain of url
        all_backlink.append(link)
        domain_temp = get_domain(link)
        if (domain_temp not in all_domain) and (domain_temp != page_domain):
            all_domain.append(domain_temp)
            
    cleanText_list = TextCleaner.clean(raw_mat["rawText"])
    word_dict = word_frequency_dict(cleanText_list)
    sorted_word_dict = dict(sorted(word_dict.items()))
    
    newid = dataPipeline.getUniqueID()
    dataPipeline.updateWebData(newid, url, sorted_word_dict, all_domain)
    dataPipeline.updateInvertedIndexing(newid, sorted_word_dict)
    dataPipeline.updateReferenceDomain(all_domain)
    
    return all_backlink
    
def removeData(url):
    """Remove Data By URL"""
    print("Removing : ", url)
    temp_datarow = dataPipeline.fetch_data_by_url(url)
    
    dataPipeline.removeWebData(temp_datarow['URL'])
    dataPipeline.uncountRef(temp_datarow['Ref_To'])
    dataPipeline.removeInvertedIndex(temp_datarow['Web_ID'], temp_datarow['All_Word'])

def scrapeLevel(origin_url, depth, depth_limit):
    # function to scrape a level and follow links
    if (depth <= depth_limit):
        # Check depth limit, if not reached, continue
        if ((linkChecker.alreadyScrape(origin_url)) == False) and (linkChecker.checkAccessibility(origin_url)):
            # Check if origin_url not is in database and accessible
            # if yes, update database
            child_url = updateLink(origin_url)

            # go deeper
            for link in child_url:
                # check if domain is the same as origin_url
                if (get_domain(link) == get_domain(origin_url)):
                    # go recursive scrapeLevel
                    print("depth : " , depth , "Scraping : ", origin_url)
                    scrapeLevel(link, depth+1, depth_limit)
        else:
            # URL is already in database
            # Check if still accessible
            if (linkChecker.checkAccessibility(origin_url)):
                # if yes , Just pass and continue ( For now? )
                pass
            else:
                # if no, Remove data from database
                removeData(origin_url)

    else:
        # Reaching the depth limit ( Base Case )
        pass


    
# main program
if __name__ == "__main__":

    # tinderURL = {
    #     "https://photographylife.com/reviews/fuji-x100f",
    #     "https://www.dpreview.com/reviews/sony-a7rv-review?utm_source=self-desktop&utm_medium=marquee&utm_campaign=traffic_source",
    #     "https://www.35mmc.com/02/02/2023/hedeco-lime-two-low-profile-shoe-mount-light-meter-review/",
    #     "https://petapixel.com/2023/02/03/canon-usa-settles-with-employees-affected-by-2020-ransomware-attack/",
    #     "https://www.35mmc.com/14/10/2021/pentax-iqzoom-928-review/"
    # }

    tinderURL = {
        "https://www.35mmc.com/02/02/2023/hedeco-lime-two-low-profile-shoe-mount-light-meter-review/"
    }

    filename = "database_test3.db"
    db_path = "project\database\\" + filename

    TextCleaner = TextCleaners()
    pageScraper = pageScrapers()
    linkChecker = LinkCheckers(db_path)
    dataPipeline = dataPipelines(db_path)
    
    depth_limit = 2
    start_depth = 1

    print("\n\nStarting . . .\n\n")
    for link in tinderURL:
        scrapeLevel(link, start_depth, depth_limit)
        
    
    print("\n\nDone\n\n")

    # close all connection to database
    dataPipelines.close()
    linkChecker.close()
