# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import json
from scrapy.exporters import JsonItemExporter

from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    """
    图片保存，并把本地路径保存到Item中
    """

    def item_completed(self, results, item, info):
        for ok, value in results:
            item["front_image_path"] = value["path"]
        return item


class JsonWithEncodingPipeline(object):
    # 自定义json导出
    def __init__(self) -> None:
        self.file = codecs.open('article.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        lines = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.closed()


class JsonExporterPipeline(object):
    # 调用scrapy提供的Json export导出json文件
    def __init__(self) -> None:
        self.file = open("articleexport.json", 'w')
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()  # 开启

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item


class MysqlPipeline(object):
    def __init__(self) -> None:
        self.conn = MySQLdb.connect('localhost', 'root', '', 'article', charset='utf8')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into articleitem(url_object_id, title, url, create_date, fav_nums) VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(insert_sql,
                            (item['url_object_id'], item["title"], item["url"], item["create_date"], item["fav_nums"]))
        self.conn.commit()
        return item

class MysqlTwistedPipeline(object):
    def __init__(self, dbpool) -> None:
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            password=settings["MYSQL_PASSWORD"],
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )

        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 采用异步的方式写入mysql
        import ArticleSpider.settings
        query = self.dbpool.runInteraction(self.do_insert, item)
        # query.addErrback(self.handle_error)

    def handle_error(self, failure, item, spider):
        print(failure)

    def do_insert(self, cursor, item):
        insert_sql = """
                    insert into articleitem(url_object_id, title, url, create_date, fav_nums) VALUES (%s, %s, %s, %s, %s)
                """
        self.dbpool.execute(insert_sql, (item['url_object_id'], item["title"], item["url"], item["create_date"], item["fav_nums"]))
