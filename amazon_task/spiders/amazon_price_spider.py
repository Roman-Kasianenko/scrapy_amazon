# -*- coding: utf-8 -*-
import scrapy
from amazon_task.items import AmazonTaskItem

class AmazonPriceSpiderSpider(scrapy.Spider):
    name = 'amazon_price_spider'
    allowed_domains = ['www.amazon.com']
    start_urls = ['http://www.amazon.com/dp/B01BEELH52', 
        'https://www.amazon.com/dp/B011L4D3BG']

    def parse(self, response):
        is_screenshot_needed = self.make_screenshoot

        if is_screenshot_needed:
            print('Save screenshoot !')

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

        if not price:
            price = self.get_price(response)

        item = AmazonTaskItem()
        item['title'] = title
        item['price'] = price
        item['discounted_price'] = discounted_price

        yield item


    def get_price(self, response):
        price = response.css('div#cerberus-data-metrics::attr(data-asin-price)').extract_first()

        if not price:
            major_value = response.css('span.buyingPrice')
            if major_value:
                minor_value = major_value.xpath('.//following-sibling::span/text()').extract_first()
                major_value = major_value.xpath('.//text()').extract_first()
                price = '{}.{}'.format(major_value, minor_value)

        if not price:
            if response.css('span#priceblock_ourprice'):
                price = response.css('span#priceblock_ourprice::text').extract_first().lstrip('$')

        return price

