import http.cookiejar as cookielib
import requests
import re

import scrapy
session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("cookie未能加载")

agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

headers = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": agent,
    "captcha_type": "cn"
}


def zhihu_login(account, password):

    if re.match("^1\d{10}", account):
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "phone_num": account,
            "password": password,
            "_xsrf": get_xsrf()
        }
    elif "@" in account:
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "email": account,
            "password": password,
            "_xsrf": get_xsrf()
        }
    response = session.post(post_url, data=post_data, headers=headers)
    print(response.content)
    session.cookies.save()


def get_xsrf():
    response = requests.get("https://www.zhihu.com/", headers=headers)
    scrapy_selector = scrapy.Selector(response=response)
    if scrapy_selector:
        _xsrf = scrapy_selector.css("input[name='_xsrf']::attr(value)").extract_first()
        return _xsrf
    else:
        return ""


def is_login():
    url = "https://www.zhihu.com/inbox"
    response = session.get(url=url, allow_redirects=False, headers=headers)
    if response.status_code == 200:
        return True
    else:
        return False


zhihu_login("13323103080", "275892441")
# get_xsrf()
is_login()
