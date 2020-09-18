# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EastmoneyItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    weight = scrapy.Field()
    share_num = scrapy.Field()
    market_value = scrapy.Field()
