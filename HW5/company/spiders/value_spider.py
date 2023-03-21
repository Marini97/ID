import scrapy
from scrapy import Selector
from urllib.parse import urljoin
from os import path
from ..parsers.ValueDataParser import ValueDataParser

class ValueSpider(scrapy.Spider):
    name = "value"
    allowed_domains = ['value.today']
    
    def start_requests(self):
        url = 'https://www.value.today/'
        yield scrapy.Request(url, self.parse)
            
    def parse(self, response):
        x = Selector(response)
        companies = response.xpath("//h2/a[contains(@href, '/company/')]/@href").extract()
        for company in companies:
            url = urljoin(response.url, company)
            yield scrapy.Request(url, callback=self.parse_company)
            
        next_page_url = response.xpath('.//span[contains(.,"Next page")]/../@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_company(self, response):
        x = Selector(response)
        item = ValueDataParser.extract_item(x, response)
        yield item