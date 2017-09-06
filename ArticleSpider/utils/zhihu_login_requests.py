import http.cookiejar as cookielib
import requests
import re

import scrapy
import time

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")



agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"

header = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": agent,
    "captcha_type": "cn"
}


def zhihu_login(account, password):
    xsrf = get_xsrf()

    try:
        session.cookies.load(ignore_discard=True)
    except:
        print("cookie未能加载")

    captcha = getcaptcha()

    if re.match("^1\d{10}", account):
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "phone_num": account,
            "password": password,
            "_xsrf": xsrf,
            "X-Xsrftoken": xsrf,
            "captcha": captcha
        }
    elif "@" in account:
        post_url = "https://www.zhihu.com/login/email"
        post_data = {
            "email": account,
            "password": password,
            "_xsrf": xsrf,
            "X-Xsrftoken": xsrf
        }
    response = session.post(post_url, data=post_data, headers=header)
    print(response.content)
    session.cookies.save()


# def analytics_web():
#     post_url = "https://zhihu-web-analytics.zhihu.com/api/v1/logs/batch"


def get_xsrf():
    response = session.get("https://www.zhihu.com/", headers=header)
    scrapy_selector = scrapy.Selector(response=response)
    if scrapy_selector:
        _xsrf = scrapy_selector.css("input[name='_xsrf']::attr(value)").extract_first()
        session.cookies.save()
        return _xsrf
    else:
        return ""


def get_index():
    response = session.get("https://www.zhihu.com", headers=header)
    with open("index_page.html", "wb") as f:
        f.write(response.text.encode(encoding="utf-8"))
    print("get_index ok")


def is_login():
    url = "https://www.zhihu.com/inbox"
    response = session.get(url=url, allow_redirects=False, headers=header)
    if response.status_code == 200:
        return True
    else:
        return False


def getcaptcha():
    captcha_url = "https://www.zhihu.com/captcha.gif?r=%d&type=login"% (time.time() * 1000)
    img = session.get(captcha_url, headers=header).content
    with open("captcha.gif", "wb") as f:
        f.write(img)
    check_code = input("请输入：")
    return check_code


zhihu_login("13323103080", "275892441")
# get_xsrf()
# is_login()
