from scrapy.cmdline import execute

import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
print(dirname)
sys.path.append(dirname)
execute(["scrapy", "crawl", "jobbole"])

# import re
# s = ' 24 收藏'
# rex = '.*?(\d+).*'
# re_match = re.match(rex, s)
# if re_match:
#     num = re_match.group(1)
#     print(num)
