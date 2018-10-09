# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AmazonTaskPipeline(object):
    def process_item(self, item, spider):
        discounted_price = item.get('discounted_price', None)
        if discounted_price:
            discount_amount = float(item.get('price')) - float(discounted_price)
            discount_percentage = (discount_amount * 100.00) / float(item.get('price'))
            discount_percentage = format(discount_percentage, '.2f') 
            item['discount_percentage'] = discount_percentage
        return item
