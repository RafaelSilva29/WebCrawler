# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

class AutoevolutionScraperPipeline:
    def process_item(self, item, spider):
        line = json.dumps(dict(item), indent=2) + ',\n'
        self.file.write(line)
        return item

    def open_spider(self, spider):
        self.file = open('autoevolution.txt', 'w')
        line = '[\n'
        self.file.write(line)

    def close_spider(self, spider):
        line = ']\n'
        self.file.write(line)
        self.file.close()
