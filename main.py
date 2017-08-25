from scrapy.cmdline import execute

import sys
import os

dirname = os.path.dirname(os.path.abspath(__file__))
# print(dirname)
sys.path.append(dirname)
execute(["scrapy", "crawl", "jobbole"])