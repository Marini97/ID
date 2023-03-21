import scrapy
from scrapy import Selector
from os import path
from ..parsers.ForbesDataParser import ForbesDataParser

class ForbesSpider(scrapy.Spider):
    name = "forbes"
    allowed_domains = ['forbes.com']
    
    def start_requests(self):
        url = 'https://www.forbes.com/companies/berkshire-hathaway/?list=global2000'
        yield scrapy.Request(url, self.parse)
            
    def parse(self, response):
        x = Selector(response)
        item = ForbesDataParser.extract_item(x, response)
        yield item
        
        next_page_url = response.xpath('//a[@class="profile-nav__next"]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
