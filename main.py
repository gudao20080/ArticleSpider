from scrapy.cmdline import execute

import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
print(dirname)
sys.path.append(dirname)
execute(["scrapy", "crawl", "jobbole"])

# import re
# s = 'http://blog.jobbole.com/112281/'
# rex = r".*?(\d{1,}).*"
# re_match = re.match(rex, s)
# if re_match:
#     num = re_match.group(1)
#     print(num)
