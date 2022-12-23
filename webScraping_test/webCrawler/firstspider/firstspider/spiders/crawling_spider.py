from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


# new class inherits from CrawlSpider class
class CrawlingSpider(CrawlSpider):
    # name for execute
    name = "toby"
    # allowed domains
    allowed_domains = ["toscrape.com"]
    # initial URL
    start_urls = ["http://books.toscrape.com/"]

    # crawl to find links that fits in rules
    # rules tuple
    rules = (
        # rule for crawling only the links that match the pattern catalouge/catagory
        Rule(LinkExtractor(allow = "catalogue/category")),
        # deny URL that have category
        Rule(LinkExtractor(allow="catalogue", deny="category"), callback="parse_item"), 
    )

    # feed from crawling
    # Extract Title, Price, Aviability
    def parse_item(self, response):
        # no return keyword, yield dictionary
        yield{
            "title" : response.css(".product_main h1::text").get(),
            "price" : response.css(".price_color::text").get(),
            # replace to format the data
            "availability" : response.css(".availability::text")[1].get().replace("\n", "").replace(" ", ""),
        }

        