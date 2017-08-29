# -*- coding: utf-8 -*-
import scrapy
import re
from ArticleSpider import items

from urllib import parse
import time


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
        # 提取文章的具体字段
        bookmark_str = response.css('.bookmark-btn::text').extract_first()
        bookmark_num = self.capture_num(bookmark_str)  # 收藏
        comment = response.css(".post-adds a span::text").extract_first()

        praise_num = response.css(".vote-post-up h10::text").extract_first(default=0)  # 赞
        comment_num = self.capture_num(comment)  # 评论数

        front_image_url = response.meta["front_image_path"]
        title = response.css(".entry-header h1::text").extract_first()
        date_str = response.css(".entry-meta-hide-on-mobile::text").extract_first().strip()
        match_result = re.match(r".*?(\d{1,}/\d{1,}/\d{1,}).*", date_str)
        if match_result:
            date_str = match_result.group(1)
        else:
            date_str = time.strftime("%Y/%m/%d", time.localtime())

        tag_list = response.css(".entry-meta-hide-on-mobile a::text").extract()

        id_rex = r".*?(\d{1,}).*"
        id_match_result = re.match(id_rex, response.url)
        url_object_id = 0
        if id_match_result:
            url_object_id = int(id_match_result.group(1))

        article_item = items.ArticleItem()
        article_item['title'] = title
        article_item['create_date'] = date_str
        article_item["url"] = response.url
        article_item["front_image_path"] = front_image_url
        article_item["front_image_url"] = parse.urljoin(response.url, front_image_url)
        article_item["praise_nums"] = praise_num
        article_item["comment_nums"] = comment_num
        article_item["fav_nums"] = bookmark_num
        article_item["tags"] = ",".join(tag_list)
        article_item["content"] = response.css(".entry").extract_first()
        article_item["url_object_id"] = url_object_id
        return article_item
