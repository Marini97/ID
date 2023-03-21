import scrapy
from scrapy import Selector
from urllib.parse import urljoin
from os import path
from ..parsers.DisfoldDataParser import DisfoldDataParser

class DisfoldSpider(scrapy.Spider):
    name = "disfold"
    allowed_domains = ['disfold.com']
    
    def start_requests(self):
        url = 'https://disfold.com/australia/companies/'
        yield scrapy.Request(url, self.parse)
            
    def parse(self, response):
        x = Selector(response)
        companies = response.xpath("//tr/td[2]/a/@href").extract()
        for company in companies:
            url = urljoin(response.url, company)
            yield scrapy.Request(url, callback=self.parse_company)
            
        next_page_url = response.xpath(".//li[contains(@class, 'active')]/following-sibling::li[1]/a/@href").extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))

    def parse_company(self, response):
        x = Selector(response)
        item = DisfoldDataParser.extract_item(x, response)
        yield item
            
            
