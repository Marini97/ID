# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    industry = scrapy.Field()
    founded = scrapy.Field()
    country = scrapy.Field()
    ceo = scrapy.Field()
    employees = scrapy.Field()
    revenue = scrapy.Field()
    pass
