from scrapy.cmdline import execute

import sys
import os

# dirname = os.path.dirname(os.path.abspath(__file__))
# print(dirname)
# sys.path.append(dirname)
# execute(["scrapy", "crawl", "jobbole"])

# import re
# s = 'http://blog.jobbole.com/112281/'
# rex = r".*?(\d{1,}).*"
# re_match = re.match(rex, s)
# if re_match:
#     num = re_match.group(1)
#     print(num)

# from datetime import datetime
# date_str = '2016/08/21'
# import time
#
# localtime = time.localtime()
# date_str = time.strftime("%Y/%m/%d", localtime)
# d = datetime.strptime(date_str, "%Y/%m/%d").date()
# print(type(d))
# print(str(d))


# class Kls(object):
#     no_inst = 0
#     def __init__(self):
#         Kls.no_inst = Kls.no_inst + 1
#
#     @classmethod
#     def get_no_of_instances(cls_obj):
#         return cls_obj.no_inst
# ik1 = Kls()
# print(ik1.get_no_of_instances())
# ik2 = Kls()
# print(ik2.get_no_of_instances())
from ArticleSpider.utils.sql import Sql

sq = Sql()
sq.select_user()