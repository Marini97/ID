# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ForbesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    link = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    ceo = scrapy.Field()
    revenue = scrapy.Field()
    founded = scrapy.Field()
    employees = scrapy.Field()
    industry = scrapy.Field()
    
