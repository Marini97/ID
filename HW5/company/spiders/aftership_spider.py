import scrapy
from scrapy import Selector
from urllib.parse import urljoin
from os import path
from ..parsers.AftershipDataParser import AftershipDataParser

class AftershipSpider(scrapy.Spider):
    name = "aftership"
    allowed_domains = ['aftership.com']
    
    def start_requests(self):
        url = 'https://www.aftership.com/store-list/top-1000-ecommerces-stores'
        yield scrapy.Request(url, self.parse)
            
    def parse(self, response):
        x = Selector(response)
        companies = response.xpath(".//td/a[contains(@href, '/top-stores/')]/@href").extract()
        for company in companies:
            url = urljoin(response.url, company)
            yield scrapy.Request(url, callback=self.parse_company)
            
        next_page_url = response.xpath(".//a[contains(@rel, 'next')]/@href").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_company(self, response):
        x = Selector(response)
        item = AftershipDataParser.extract_item(x, response)
        yield item