# -*- coding: utf-8 -*-
import scrapy
import re


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']




    def parse(self, response):
        bookmark_str = response.css('.bookmark-btn::text').extract_first()
        bookmark_num = self.filterNum(bookmark_str) #收藏
        comment = response.css(".post-adds a span::text").extract_first()

        praise_num = response.css(".vote-post-up h10::text").extract_first()    #赞
        comment_num = self.filterNum(comment)   #评论数

        return bookmark_num;

    def filterNum(self, s: str):
        rex = '.*?(\d+).*'
        match_result = re.match(rex, s)
        if match_result:
            num = match_result.group(1)
            return num

        return 0
