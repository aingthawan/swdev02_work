from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
import re

class page_scrapers:
    """Class for Scrape single page, Return dictionary URL, all backlinks and Raw Text"""
    def __init__(self):
        # Set header
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

    def get_raw_html(self, url):
        """get raw html soup obj using a rotating proxy"""
        res_temp = requests.get(url, headers=self.headers)
        return res_temp.text
    
    def scrape_raw_text(self, html_text):
        """Return raw text string from bs4 object"""
        soup = BeautifulSoup(html_text, 'html.parser')
        text_content = soup.get_text()        
        text_content = text_content.strip()
        return text_content
    
    # tested
    def scrape_all_urls(self, html_text):
        soup = BeautifulSoup(html_text, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            url = link['href']
            if re.match(r'^https?://', url) and not re.search(r'\.(jpg|jpeg|png|gif)$', url):
                urls.add(url)
        return list(urls)

    # just a combination of above two methods, no testing
    def scrape_page(self, url):
        """Return a dictionary of url, all unrepeated backlinks and raw text"""
        raw_soup_html = self.get_raw_html(url).text
        # if not none
        if raw_soup_html is not None:
            return {
                "url" : url,
                "backlinks" : self.scrape_all_urls(raw_soup_html),
                "rawText" : self.scrape_raw_text(raw_soup_html)
            }
        else:
            return None
 