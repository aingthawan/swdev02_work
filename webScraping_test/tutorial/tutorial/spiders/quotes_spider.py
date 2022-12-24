# build this spider'

import scrapy

class QuotesSpider(scrapy.Spider):
    
    # initial request for start crawling
    def start_requests(self):
        # specific name for spider
        name = "quotes"
        # urls lists
        urls = [
            'https://quotes.toscrape.com/page/1/',
            'https://quotes.toscrape.com/page/2/',
        ]        
    
    # response function for handle each requests
    # extract the scraped data
    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        # self.log(f'Saved file {filename}')
