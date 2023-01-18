# File for class pageScraper
# For scrape single page, Return dictionary URL, all backlinks and Raw Text
# Input : url   ------>>  Output : {
                                #     "url" : url,
                                #     "backlinks" : self.scrape_all_urls(raw_soup_html),
                                #     "rawText" : self.scrape_raw_text(raw_soup_html)
                                # }
# To Use : obj.scrape_page(url)
# 
# dev : Aingkk.
#                UML Diagram
#                +-----------------------------------+
#                | pageScraper                       |
#                +-----------------------------------+
#                | -allowed_domain: list             |
#                +-----------------------------------+
#                | +__init__()                       |
#                | +get_raw_html(url: str)           |
#                | +scrape_raw_text(soup_obj: bs4)   |
#                | +scrape_all_urls(soup_obj: bs4)   |
#                | +scrape_page(url: str)            |
#                +-----------------------------------+

import validators
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class pageScraper:
    """Class for Scrape single page, Return dictionary URL, all backlinks and Raw Text"""
    def __init__(self):
        # Set allowed domain
        self.allowed_domain = [
            "artyt.me",
            "www.35mmc.com",
            "www.dpreview.com"
        ]
    
    def get_raw_html(self, url):
        """get raw html soup obj"""
        # webReq = requests.get(url)
        return BeautifulSoup((requests.get(url)).text, "html.parser")
    
    def scrape_raw_text(self, soup_obj):
        """Return raw text string from bs4 boject"""
        return ' '.join([raw.text for raw in soup_obj.find_all(['h1', 'p'])])
    
    def scrape_all_urls(self, soup_obj):
        """Return list of all URLs string from bs4 object"""
        return_url = []
        for url_obj in soup_obj.find_all('a'):
            url = url_obj.get('href')
            if (url is not None) and validators.url(url) and (url not in return_url) and ((urlparse(url).netloc) in self.allowed_domain):
                return_url.append(url)
                # print(url)
                # print(urlparse(url).netloc)
        return return_url
    
    def scrape_page(self, url):
        """Return a dictionary of url, all unrepeated backlinks and raw text"""
        raw_soup_html = self.get_raw_html(url)
        return {
            "url" : url,
            "backlinks" : self.scrape_all_urls(raw_soup_html),
            "rawText" : self.scrape_raw_text(raw_soup_html)
        }
        