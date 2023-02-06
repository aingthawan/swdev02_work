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
    newid = dataPipeline.getUniqueID()
    raw_mat = pageScraper.scrape_page(url)
    
    all_backlinks = raw_mat["backlinks"]

    page_domain = get_domain(url)

    all_domain = [] # <<<<<<<<< All domain

    for link in all_backlinks:
        # get domain of url
        domain_temp = get_domain(link)
        if (domain_temp not in all_domain):
            all_domain.append(domain_temp)
            
    cleanText_list = TextCleaner.clean(raw_mat["rawText"])
    word_dict = word_frequency_dict(cleanText_list)
    sorted_word_dict = dict(sorted(word_dict.items()))
    
    dataPipeline.updateReferenceDomain(all_domain)
    dataPipeline.updateWebData(newid, url, sorted_word_dict, all_domain)
    dataPipeline.updateInvertedIndexing(newid, sorted_word_dict)
    
def removeData(url):
    """Remove Data By URL"""
    print("Removing : ", url)
    temp_datarow = dataPipeline.fetch_data_by_url(url)
    
    dataPipeline.removeWebData(temp_datarow['URL'])
    dataPipeline.uncountRef(temp_datarow['Ref_To'])
    dataPipeline.removeInvertedIndex(temp_datarow['Web_ID'], temp_datarow['All_Word'])

# main program
if __name__ == "__main__":

    tinderURL = {
        "https://photographylife.com/reviews/fuji-x100f",
        "https://www.dpreview.com/reviews/sony-a7rv-review?utm_source=self-desktop&utm_medium=marquee&utm_campaign=traffic_source",
        "https://www.35mmc.com/13/01/2018/nikon-f75-review-project-pt-4/"
    }

    db_path = "database\database_1.db"

    TextCleaner = TextCleaners()
    pageScraper = pageScrapers()
    linkChecker = LinkCheckers(db_path)
    dataPipeline = dataPipelines(db_path)

    for starter in tinderURL:
        # if link is not in database
        if (linkChecker.alreadyScrape(starter) == False):
            # scrape and update database
            updateLink(starter)
            print("Scraped: " + starter)
        else:
            print("Already Scraped: " + starter)
            # check if still accessible
            if (linkChecker.checkAccessibility(starter) == False):
                removeData(starter)
            else:
                pass