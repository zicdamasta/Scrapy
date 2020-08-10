# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RimiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    currency = scrapy.Field()
    bonuscard_price = scrapy.Field()
    url = scrapy.Field()
    pic_url = scrapy.Field()
