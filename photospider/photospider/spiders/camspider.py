# Reference : https://www.youtube.com/watch?v=o1g8prnkuiQ&ab_channel=freeCodeCamp.org

import scrapy
# another spider option + rules
from scrapy.spiders import CrawlSpider, Rule
# with links extractor, for rules set up
from scrapy.linkextractors import LinkExtractor

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
        Rule(LinkExtractor(allow='/category/reviews-experinces/slrs/'), callback='parse_item', follow=True)
    ]

    def parse_item(self, response):
        yield response