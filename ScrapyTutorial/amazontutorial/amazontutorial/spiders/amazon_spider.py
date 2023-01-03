import scrapy
from ..items import AmazontutorialItem


class AmazonSpiderSpider(scrapy.Spider):
    name = 'amazon_spider'
    # allowed_domains = ['amazon.com']
    start_urls = [
        'https://www.amazon.com/s?rh=n%3A27&fs=true&ref=lp_27_sar'
    ]

    page_number = 1

    def parse(self, response):
        items = AmazontutorialItem()

        product_name = response.css('.a-size-medium::text').extract()
        # multiple class css selector
        product_author = response.css('.a-color-secondary .a-row .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.s-link-style').css('::text').extract()
        product_price = response.css('.s-price-instructions-style .a-price span span').css('::text').extract()
        product_imagelink = response.css('.s-image-fixed-height::attr(src)').extract()

        items['product_name'] = product_name
        items['product_author'] = product_author
        items['product_price'] = product_price
        items['product_imagelink'] = product_imagelink

        next_page = "https://www.amazon.com/s?i=stripbooks&rh=n%3A27&fs=true&page=" + str(AmazonSpiderSpider.page_number) + "&qid=1672744914&ref=sr_pg_1"

        if AmazonSpiderSpider.page_number <= 75:
            AmazonSpiderSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)