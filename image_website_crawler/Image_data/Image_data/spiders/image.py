# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.loader import ItemLoader
from Image_data.items import ImageDataItem



class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['behindwoods.com']
    start_urls = ['http://behindwoods.com/hindi-actor/actor-photos-stills.html']

    def parse(self, response):
        actors = response.xpath('//*[@class="full-width float top_margin_10 tab-cntr"]/ul/li/span/a/@href').extract()
        for actor in actors:
            actor = actor.replace('//www.','http://')
            yield Request(actor,callback=self.parse_actor)

    def parse_actor(self,response):
        l = ItemLoader(item=ImageDataItem(),response=response)
        title = response.xpath('//h1/text()').extract()[0]
        title = title.split()
        title.pop()
        title = " ".join(title)

        image_urls = response.xpath('//*[@class="grey_border margin_btm_5"]/@src').extract()
        if len(image_urls)==0:
            image_urls = []
            url = response.xpath('//*[@id="slideshow"]/span/a/img/@src').extract()[0]
            url = url.replace('https://www.','http://')
            num = ''.join([x for x in url if x.isdigit()])
            numbers = [y for y in range(1,11)]
            image_urls = [url.replace(num,str(int(num)-z)) for z in numbers]
        else:
            image_urls = [('http://behindwoods.com'+url) for url in image_urls]
        print(len(image_urls))
        print(image_urls)


        l.add_value('title',title)
        l.add_value('image_urls_urls',image_urls)
        l.add_value('image_urls',[img for img in image_urls])
        print(title,image_urls)

        return l.load_item()
