# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import time
from datetime import datetime
import scrapy
import re
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()


def captureDate(date_str):
    match_result = re.match(r".*?(\d{1,}/\d{1,}/\d{1,}).*", date_str)
    if match_result:
        date_str = match_result.group(1)
    else:
        date_str = time.strftime("%Y/%m/%d", time.localtime())

    try:
        create_date = datetime.strptime(date_str, "%Y/%m/%d").date()
    except:
        date_str = time.strftime("%Y/%m/%d", time.localtime())
        create_date = datetime.strptime(date_str, "%Y/%m/%d").date()

    return create_date


def capture_num(s):
    rex = '.*?(\d+).*'
    match_result = re.match(rex, s)
    if match_result:
        num = match_result.group(1)
        return int(num)

    return 0


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(lambda x: x + "-jobbole"),
    )
    create_date = scrapy.Field(
        input_processor=MapCompose(captureDate),

    )
    url = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(lambda x: x)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(capture_num),

    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(capture_num),
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(capture_num),
    )
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    content = scrapy.Field(
    )
    url_object_id = scrapy.Field(
        input_processor=MapCompose(capture_num, str),
    )



