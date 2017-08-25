# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader

from ArticleSpider.items import TestItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/']

    def parse(self, response):
        l = ItemLoader(item=TestItem(), response=response)
        l.add_xpath("id", '//div[@class="product_name"]')
        l.add_css("stock", 'p#stock')

        return l.load_item()

    def start_requests(self):


        yield scrapy.Request("ddd", callback=self.parse)
        return super().start_requests()
