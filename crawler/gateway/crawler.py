import pandas
import requests
from bs4 import BeautifulSoup

html = requests.get('https://finance.naver.com/item/main.nhn?code=005930')
bs_obj = BeautifulSoup(html.content, "html.parser")

no_today = bs_obj.find("p", {"class": "no_today"})
blind = no_today.find("span", {"class": "blind"})

# print(bs_obj)
print(no_today)
# print(blind.text)
