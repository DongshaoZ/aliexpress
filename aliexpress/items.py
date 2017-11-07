# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class AliexpressItem(Item):
    category = Field()
    sub_category = Field()
    name = Field()
    url = Field()
    img = Field()
    price = Field()
    rate_percent = Field()
    rate_num = Field()
    order_num = Field()




