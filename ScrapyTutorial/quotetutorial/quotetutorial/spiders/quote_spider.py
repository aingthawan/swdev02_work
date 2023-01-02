# spider from scrapy
# for scrape only title from the given website
# quote to scrape, in this case
# to start : "scrapy crawl quotes" at the top dir of project

import scrapy
# import class from other file, items.py in this case
from ..items import QuotetutorialItem

#  class inherited from scrapy.Spider
class QuoteSpider(scrapy.Spider):
    # name of spider
    name = 'quotes'

    # list of URLs to scrape
    start_urls = [
        'https://quotes.toscrape.com/'
    ] 

    # method to parse the response
    def parse(self, response):
        # create instance of class QuotetutorialItem
        items = QuotetutorialItem()

        all_div_quotes = response.css('div.quote')

        # loop through each quotes in all_div_quotes
        for quotes in all_div_quotes:
            title = quotes.css('span.text::text').extract()
            author = quotes.css('.author::text').extract()
            tags = quotes.css('.tag::text').extract()

            # send data to items.py (temporary container)
            items['title'] = title
            items['author'] = author
            items['tags'] = tags

            # YEET! to pipelines.py
            yield items