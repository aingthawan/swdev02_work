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

class pageScrapers:
    """Class for Scrape single page, Return dictionary URL, all backlinks and Raw Text"""
    def __init__(self):
        # Set header
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        # self.proxies = self.read_proxies_from_file("project\src\proxy\proxy_valid.txt")
    
    # Dead method
    def read_proxies_from_file(self, filename):
        """Read proxies from a file and return as a list"""
        proxies = []
        with open(filename, "r") as f:
            for line in f:
                proxies.append(line.strip())
        return proxies
    
    def get_raw_html(self, url):
        """get raw html soup obj using a rotating proxy"""
        res_temp = requests.get(url, headers=self.headers)
        if res_temp.status_code == 200:
            return res_temp.text
        else:
            return None
    
    def scrape_raw_text(self, html_text):
        """Return raw text string from bs4 boject"""
        soup = BeautifulSoup(html_text, 'html.parser')
        return soup.get_text()
    
    # def scrape_all_urls(self, html_text):
    #     soup = BeautifulSoup(html_text, 'html.parser')
    #     urls = []
    #     for link in soup.find_all('a'):
    #         url = link.get('href')
    #         if url and re.match("^(http://|https://)", url) and not re.search(".(jpg|jpeg|png|gif)$", url):
    #             urls.append(url)
    #     return list(set(urls))
    
    def scrape_all_urls(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            url = link['href']
            if re.match(r'^https?://', url) and not re.search(r'\.(jpg|jpeg|png|gif)$', url):
                urls.add(url)
        return list(urls)

    def scrape_page(self, url):
        """Return a dictionary of url, all unrepeated backlinks and raw text"""
        raw_soup_html = self.get_raw_html(url).text
        return {
            "url" : url,
            "backlinks" : self.scrape_all_urls(raw_soup_html),
            "rawText" : self.scrape_raw_text(raw_soup_html)
        }
 