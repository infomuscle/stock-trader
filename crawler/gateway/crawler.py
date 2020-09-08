import requests
from bs4 import BeautifulSoup

urlBody = "https://finance.naver.com/item"

samsung_electronics = "005930"


def get_url(tab_name, company_code):
    url = urlBody
    url += "/" + tab_name + ".nhn"
    url += "?code=" + company_code

    return url


def get_soup(url):
    html_doc = requests.get(url)
    soup = BeautifulSoup(html_doc, "html.parser")

    return soup


def get_current_price(company_code):
    url = get_url("sise", company_code)
    soup = get_soup(url)

    current_price = soup.find("strong", {"id": "_nowVal"})

    return current_price.text


print(get_current_price(samsung_electronics))
