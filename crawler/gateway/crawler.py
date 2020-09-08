import json
import logging
import re

import requests
from bs4 import BeautifulSoup

urlBody = "https://finance.naver.com/item"
samsung_electronics = "005930"

logger = logging.getLogger()


def get_url(tab_name, company_code):
    url = urlBody
    url += "/" + tab_name + ".nhn"
    url += "?code=" + company_code

    return url


def get_soup(tab_name, company_code):
    url = get_url(tab_name, company_code)
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup


def get_soup_by_url(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup


def get_current_price(company_code):
    soup = get_soup("sise", company_code)

    current_price = soup.find("strong", {"id": "_nowVal"})

    return current_price.text


def get_daily_prices_to_page(company_code, page):
    daily_price_infos = {}

    for p in range(1, int(page) + 1):
        daily_price_infos.update(get_daily_prices_of_page(company_code, p))

    return daily_price_infos


def get_daily_prices_of_page(company_code, page):
    daily_price_infos = {}

    url = get_url("sise_day", company_code)
    url += "&page=" + str(page)
    soup = get_soup_by_url(url)

    base_table = soup.find_all("tr")
    price_table = base_table[2:7] + base_table[10:-2]
    for daily_price_info in price_table:
        price_datas = daily_price_info.find_all("span")

        img = str(daily_price_info.find("img"))
        rate = get_rate_sign(img) + re.sub('[\t\n]', '', price_datas[2].text)

        price_info = {}
        price_info["closing"] = price_datas[1].text
        price_info["rate"] = rate
        price_info["opening"] = price_datas[3].text
        price_info["highest"] = price_datas[4].text
        price_info["lowest"] = price_datas[5].text
        price_info["volume"] = price_datas[6].text

        daily_price_infos[price_datas[0].text] = price_info

    return daily_price_infos


def get_rate_sign(img):
    sign = ""
    if "ico_up" in img:
        sign = "+"
    elif "ico_down" in img:
        sign = "-"

    return sign


# print(get_current_price(samsung_electronics))
# print(get_daily_prices(samsung_electronics))
# print(json.dumps(get_daily_prices(samsung_electronics)))
print(json.dumps(get_daily_prices_to_page(samsung_electronics, 10)))
