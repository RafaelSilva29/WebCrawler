# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AutoevolutionScraperItem(scrapy.Item):
    brand = scrapy.Field()
    model = scrapy.Field()
