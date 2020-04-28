# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from actors_data.items import ActorsDataItem
from wikipedia.exceptions import PageError
import wikipedia
import os


def getsummary(title):

    try:
        summary = wikipedia.summary(title)
    except PageError:
        title = title.split()
        title = '{}({})'.format(title[1],title[0])
        summary = wikipedia.summary(title)
    return summary

class ActorSpider(scrapy.Spider):
    name = 'actor'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/wiki/List_of_Indian_film_actresses']

    def parse(self, response):
        actors = response.xpath('//*[@class="div-col columns column-width"]/ul/li/a/@href').extract()

        for actor in actors:

            url = 'http://en.wikipedia.org' + actor


            yield Request(url,callback=self.parse_actors)

    def parse_actors(self,response):

        l = ItemLoader(item=ActorsDataItem(),response=response)

        title = response.xpath('//*[@class="firstHeading"]/text()').extract()[0]
        summary = getsummary(title)
        url_list = response.xpath('//*[@class="image"]/img/@src').extract()
        if len(url_list) == 0:
            url = "No Images Found"
        elif len(url_list)==1:
            url = url_list[0]
        elif len(url_list)>1 and url_list[0]=='//upload.wikimedia.org/wikipedia/commons/thumb/a/a6/India_film_clapperboard_%28variant%29.svg/30px-India_film_clapperboard_%28variant%29.svg.png':
            url = url_list[1]
        else:
            url = url_list[0]
        print(url)
        image_urls = url.replace("//","http://")
        #image_url = 'http://'+ image_url
        print(title)
        #print(os.getcwd())
        #yield{
        #'Title':title,
        #"summary":summary,
        #"Image_url":image_url,
        #}
        l.add_value('title',title)
        l.add_value('summary',summary)
        l.add_value('image_urls',image_urls)

        return l.load_item()
