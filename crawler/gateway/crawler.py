import requests
import json
from bs4 import BeautifulSoup

urlBody = "https://finance.naver.com/item"
samsung_electronics = "005930"


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


def get_daily_prices(company_code, page):
    return


def get_daily_prices_by_page(company_code):
    daily_prices = {}

    soup = get_soup("sise_day", company_code)

    base_table = soup.find_all("tr")
    price_table = base_table[2:7] + base_table[10:-2]
    for daily_info in price_table:
        price_datas = daily_info.find_all("span")
        price_info = {}
        price_info["closing"] = price_datas[1].text
        price_info["rate"] = price_datas[2].text
        price_info["opening"] = price_datas[3].text
        price_info["highest"] = price_datas[4].text
        price_info["lowest"] = price_datas[5].text
        price_info["volume"] = price_datas[6].text

        daily_prices[price_datas[0].text] = price_info

    return daily_prices

# print(get_current_price(samsung_electronics))
# print(get_daily_prices(samsung_electronics))
# print(json.dumps(get_daily_prices(samsung_electronics)))
