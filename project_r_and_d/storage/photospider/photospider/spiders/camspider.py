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
        # 'https://www.35mmc.com/'
        'https://www.35mmc.com/28/12/2022/nikon-fm2-camera-review/'
    ]

    # main page
    # https://www.35mmc.com/
    # links to slr reviews archive
    # https://www.35mmc.com/category/reviews-experinces/slrs/
    # rules = [
    #     Rule(LinkExtractor(allow='/category/reviews-experinces/'), callback='parse_item', follow=True)
    # ]

    def parse_item(self, response):
        items = PhotospiderItem()
        related_url = []
        related_url_text = ''

        # list of raw html
        raw_request = response.css('article').get()

        items['title'] = response.css('.entry-title::text').get()    
        items['url'] = response.request.url

        backlink_list = response.css('.item-related a::attr(href)').extract()
        i = 0
        while i < len(backlink_list):
            related_url.append(backlink_list[i])
            related_url_text += backlink_list[i] + ' '
            i += 2
        items['related_url'] = related_url_text

        items['raw_html'] = response.css('article').get()

        yield items
        # yield{
        #     'title': response.css('.entry-title::text').get(),
        #     'url': response.css('.item-related a::attr(href)').get(),
        #     'related_url': related_url_text,
        #     'raw_html': response.css('article').get()
        # }

    def follow_link(self, url_list):
        for url in url_list:
            yield scrapy.Request(url, callback=self.parse_item)
