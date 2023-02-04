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
import re

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
        return requests.get(url)
    
    def scrape_raw_text(self, html_text):
        """Return raw text string from bs4 boject"""
        # return ' '.join([raw.text for raw in soup_obj.find_all(['h1', 'p'])])
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    
    def scrape_all_urls(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        urls = []
        for link in soup.find_all('a'):
            url = link.get('href')
            if url and re.match("^(http://|https://)", url) and not re.search(".(jpg|jpeg|png|gif)$", url):
                urls.append(url)
        return list(set(urls))
    
    def scrape_page(self, url):
        """Return a dictionary of url, all unrepeated backlinks and raw text"""
        raw_soup_html = self.get_raw_html(url).text
        return {
            "url" : url,
            "backlinks" : self.scrape_all_urls(raw_soup_html),
            "rawText" : self.scrape_raw_text(raw_soup_html)
        }

            