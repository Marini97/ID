# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class AftershipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    
    name = scrapy.Field()
    founded = scrapy.Field()
    employees = scrapy.Field()
    monthly_sales = scrapy.Field()
    headquarters = scrapy.Field()
    speed_score = scrapy.Field()
    
