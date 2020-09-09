import logging
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from gateway import constants

logger = logging.getLogger()

url_body = "https://finance.naver.com/item"
samsung_electronics = "005930"


def get_url(tab_name: str, params: dict):
    url = url_body
    url += "/" + tab_name + ".nhn"

    if (len(params.keys()) > 0):
        for i, k in enumerate(params.keys()):
            url += "?" if i == 0 else "&"
            url += k + "=" + params[k]

    return url


def get_soup(url):
    headers = {
        "User-Agent": constants.HEADER_VALUE_USER_AGENT}
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup


def get_current_price(code: str):
    params = dict()
    params["code"] = code

    url = get_url("sise", params)
    soup = get_soup(url)

    current_price = soup.find("strong", {"id": "_nowVal"})

    return current_price.text


def get_daily_prices_to_page(code, page):
    daily_price_infos = dict()

    for p in range(1, int(page) + 1):
        daily_price_infos.update(get_daily_prices_of_page(code, p))

    return daily_price_infos


def get_daily_prices_of_page(code, page):
    params = dict()
    params["code"] = code
    params["page"] = str(page)

    url = get_url("sise_day", params)
    soup = get_soup(url)

    base_table = soup.find_all("tr")
    price_table = base_table[2:7] + base_table[10:-2]

    daily_price_infos = dict()
    for daily_price_info in price_table:
        price_data = daily_price_info.find_all("span")

        price_info = get_price_info(price_data)

        img = str(daily_price_info.find("img"))
        rate = get_rate_sign(img) + re.sub("[\t\n]", "", price_data[2].text)
        price_info["rate"] = rate

        daily_price_infos[price_data[0].text] = price_info

    return daily_price_infos


def get_price_info(price_data):
    price_info = dict()
    price_info["closing"] = price_data[1].text
    price_info["opening"] = price_data[3].text
    price_info["highest"] = price_data[4].text
    price_info["lowest"] = price_data[5].text
    price_info["volume"] = price_data[6].text
    return price_info


def get_rate_sign(img):
    sign = ""
    if "ico_up" in img:
        sign = "+"
    elif "ico_down" in img:
        sign = "-"

    return sign


def get_code_list():
    df = pd.read_html(constants.URL_KRX_CODE_LIST, header=0)[0]
    df.종목코드 = df.종목코드.map("{:06d}".format)
    df = df[["회사명", "종목코드"]]
    df = df.rename(columns={"회사명": "name", "종목코드": "code"})


def get_per(code: str):
    params = dict()
    params["code"] = code

    url = get_url("sise", params)
    soup = get_soup(url)

    per = soup.find("span", {"id": "_sise_per"})
    per = re.sub("[\t\n]", "", per.text)
    return per

# if __name__ == "__main":
# print(get_current_price(samsung_electronics))
# print(json.dumps(get_daily_prices_to_page(samsung_electronics, 10)))
# print(get_per(samsung_electronics))
