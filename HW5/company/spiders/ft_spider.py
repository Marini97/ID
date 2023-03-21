import scrapy
from scrapy import Selector
from urllib.parse import urljoin
from os import path
from ..parsers.FtDataParser import FtDataParser

class FtSpider(scrapy.Spider):
    name = "ft"
    allowed_domains = ['ft.com']
    
    def start_requests(self):
        url = 'https://www.ft.com/ft1000-2022'
        yield scrapy.Request(url, self.parse)
            
    def parse(self, response):
        x = Selector(response)
        for i in range (2,1002):
            item = FtDataParser.extract_item(x, response, i)
            yield item
            
            
