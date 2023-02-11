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
    page_number = 2

    # list of URLs to scrape
    start_urls = [
        'https://quotes.toscrape.com/page/1/'
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

        # get next button URL
        # next_page = response.css('li.next a::attr(href)').get()
        next_page = "https://quotes.toscrape.com/page/" + str(QuoteSpider.page_number) + "/"
        # if next button exist, go to next page
        # if next_page is not None:
        if QuoteSpider.page_number < 11:
            # use funcution response.follow to go to next page 
            # (go back to parse)
            QuoteSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)