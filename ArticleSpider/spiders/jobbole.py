# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
import re
import time
from _datetime import datetime
from urllib import parse
from scrapy.loader.processors import TakeFirst
import scrapy

from ArticleSpider import items


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 1.获取文章列表，并解析

        # 2.提取所有文章的url,提交给scrapy进行下载
        post_nodes = response.css(".post.floated-thumb")
        for post_node in post_nodes:
            image_url_path = post_node.css("div a img::attr(src)").extract_first()
            # article_url = post_node.css(".post-meta .read-more a::attr(href)").extract_first()
            article_url_path = post_node.css(".read-more a::attr(href)").extract_first()
            yield scrapy.Request(url=parse.urljoin(response.url, article_url_path), callback=self.parse_detail,
                                 meta={"front_image_path": image_url_path})

        # 提取下一页
        next_page_url = response.css(".next.page-numbers::attr(href)").extract_first()
        if next_page_url:
            yield scrapy.Request(parse.urljoin(response.url, next_page_url), parse)

    def capture_num(self, s: str):
        rex = '.*?(\d+).*'
        match_result = re.match(rex, s)
        if match_result:
            num = match_result.group(1)
            return num

        return 0

    def parse_detail(self, response):
        """
            解析文章
        :param response:
        :return:
        """
        item_loader = JobBoleArticleLoader(item=items.JobBoleArticleItem(), response=response)
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("create_date", ".entry-meta-hide-on-mobile::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("front_image_url", [parse.urljoin(response.url, response.meta["front_image_path"])])
        item_loader.add_css("praise_nums", ".vote-post-up h10::text")
        item_loader.add_css("comment_nums", ".post-adds a span::text")
        item_loader.add_css("fav_nums", ".bookmark-btn::text")
        item_loader.add_css("tags", ".entry-meta-hide-on-mobile a::text")
        item_loader.add_css("content", ".entry")
        item_loader.add_value("url_object_id", response.url)

        item = item_loader.load_item()
        return item


class JobBoleArticleLoader(ItemLoader):
    default_output_processor = TakeFirst()
