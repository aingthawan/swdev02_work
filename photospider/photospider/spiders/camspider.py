# Reference : https://www.youtube.com/watch?v=o1g8prnkuiQ&ab_channel=freeCodeCamp.org

import scrapy
# another spider option + rules
from scrapy.spiders import CrawlSpider, Rule
# with links extractor, for rules set up
from scrapy.linkextractors import LinkExtractor

from ..items import PhotospiderItem

import json

class photospiderSpider(CrawlSpider):
    # CrawlSpider need a rules to follow 
    # and a parse function to parse with didn't name parse
    name = "camspider"
    allowed_domains = ["35mmc.com"]

    start_urls = [
        'https://www.35mmc.com/'
    ]

    # main page
    # https://www.35mmc.com/
    # links to slr reviews archive
    # https://www.35mmc.com/category/reviews-experinces/slrs/
    rules = [
        Rule(LinkExtractor(allow='/category/reviews-experinces/(slrs|medium-format)/'), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        items = PhotospiderItem()

        # list of raw html
        raw_request = response.css('article')

        for element in raw_request:

            items['title'] = element.css('.entry-title a::text')[0].extract()
            items['category'] = element.css('span.cat').css('a::text')[0].extract()
            items['link'] = element.css('.entry-title a::attr(href)')[0].extract()
            yield items
