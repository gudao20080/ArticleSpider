import pymysql
from ArticleSpider import settings

connection = pymysql.connect(host=settings.MYSQL_HOST,  user=settings.MYSQL_USER, port=3306, passwd=""
                             , db=settings.MYSQL_DBNAME, charset="utf8")
# 通过cursor创建游标
cursor = connection.cursor()


class Sql:
    @classmethod
    def insert_dd_name(cls, xs_name, xs_author, category):
        sql = "INSERT INTO add_name (id ,xs_name,s_author , category) VALUES (NULL ,%s ,%s ,%s)"
        value = (xs_name, xs_author, category)
        cursor.execute(sql, value)
        # 提交SQL
        connection.commit()

    # @classmethod
    def select_user(self):
        sql = "SELECT * FROM articleitem"
        cursor.execute(sql)
        data = cursor.fetchall()
        for i in data:
            print(i)