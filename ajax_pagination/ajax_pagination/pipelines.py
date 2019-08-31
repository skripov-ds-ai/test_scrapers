# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pandas.io.json import json_normalize



class AjaxPaginationPipeline(object):
    items = []

    def open_spider(self, spider):
        self.items = []

    def process_item(self, item, spider):
        self.items.append(item)
        return item

    def close_spider(self, spider):
        df = json_normalize(self.items)
        df.to_csv('ajax_data.csv', index=False)
        spider.logger.info('Spider closed in pipeline: %s', spider.name)


