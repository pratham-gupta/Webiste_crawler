# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

class ImageDataPipeline(object):
    def process_item(self, item, spider):
        os.chdir('C:/Users/Pratham Gupta/Desktop/actor_image_only')

        for i in range(len(item['image_urls_urls'])):

            if item['images'][i]['path']:
                title = item['title'][0]
                new_image_name = item['title'][0]+'{}'.format(i)+'.jpg'
                if not os.path.isdir('full/{}'.format(title)):
                    os.mkdir('full/{}'.format(title))
                else:
                    pass

                new_image_path = 'full/{}/'.format(title)+new_image_name

                os.rename(item['images'][i]['path'],new_image_path)
