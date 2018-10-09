# -*- coding: utf-8 -*-
import scrapy
from amazon_task.items import AmazonTaskItem

class AmazonPriceSpiderSpider(scrapy.Spider):
    name = 'amazon_price_spider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/dp/B01BEELH52']

    def parse(self, response):
        title = response.css('span#productTitle::text').extract_first()
        promo = response.xpath('//input[@data-discounted-price]')
        discounted_price = None
        price = None
        if promo:
        	discounted_price = promo.css('::attr(data-discounted-price)').extract_first()
        	price = promo.css('::attr(data-buying-price)').extract_first()

        if title:
            title = title.strip()

        if not price:
        	price_div = response.css('div#price')
        	price = price_div.css('span.a-text-strike::text').extract_first()

        item = AmazonTaskItem()
        item['title'] = title
        item['price'] = price
        item['discounted_price'] = discounted_price

        yield item

