# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class AliexpressPipeline(object):
    def __init__(self):
        self.file = open('product.txt', mode='w', encoding='utf-8')

    def process_item(self, item, spider):
        data = json.dumps(dict(item)) + '\n'
        self.file.write(data)

    def close_spider(self, spider):
        self.file.close()
