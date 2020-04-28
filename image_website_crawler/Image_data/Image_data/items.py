# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImageDataItem(scrapy.Item):
    title = scrapy.Field()
    image_urls_urls = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
