import scrapy
from scrapy import Selector
from urllib.parse import urljoin
from os import path
from selenium import webdriver
from ..parsers.ForbesDataParser import ForbesDataParser

class Forbes2Spider(scrapy.Spider):
    name = "forbes2"
    allowed_domains = ['forbes.com']
    
    """def start_requests(self):
        with open("dataset/forbes.txt", "rt") as f:
            start_urls = [url.strip() for url in f.readlines()]
        for url in start_urls:
            yield scrapy.Request(url, self.parse_company)"""
    
    def __init__(self):
        self.driver = webdriver.Chrome()
        
    def start_requests(self):
        url = 'https://www.forbes.com/lists/global2000/'
        yield scrapy.Request(url, self.parse)

            
    def parse(self, response):
        self.driver.get(response.url)
        
        while True:
            next = self.driver.find_element_by_xpath('//button[1]')
            try:
                next.click()
                # get the data and write it to scrapy items
            except:
                break  
        x = Selector(response)
        companies = self.driver.find_elements_by_xpath("//a[contains(@href, '/companies/')]")
        for company in companies:
            url = urljoin(response.url, company)
            yield scrapy.Request(url, callback=self.parse_company)
        
    def parse_company(self, response):
        x = Selector(response)
        item = ForbesDataParser.extract_item(x, response)
        yield item