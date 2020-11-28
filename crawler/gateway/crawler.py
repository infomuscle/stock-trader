import logging
import re
from datetime import date
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from gateway import constants as consts
from gateway.models import *

logger = logging.getLogger()


def get_url(tab_name: str, params: dict):
    """
    네이버 증권 URI에 탭 이름과 파라미터를 붙어 네이버 증권 URL 생성
    @return url: str
    """
    url = consts.URL_BODY_NAVER
    url += tab_name + ".nhn"

    if (len(params.keys()) > 0):
        for i, k in enumerate(params.keys()):
            url += "?" if i == 0 else "&"
            url += k + "=" + params[k]

    return url


def get_soup(url):
    """
    User-Agent가 포함된 HTTP 헤더와 URL로 BeautifulSoup 생성
    @return soup: BeautifulSoup
    """
    headers = {"User-Agent": consts.HEADER_VALUE_USER_AGENT}
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup


def get_current_price(code: str):
    """
    종목코드의 현재 가격 조회
    @return current_price: str
    """
    params = dict()
    params["code"] = code

    url = get_url("item/sise", params)
    soup = get_soup(url)

    current_price = soup.find("strong", {"id": "_nowVal"})

    return current_price.text


class CompanyDetailCrawler:

    def get_indicators(self, code: str):

        url = consts.URL_BODY_NAVER_COMPANY + code
        soup = get_soup(url)

        table = soup.find("td", {"class": "td0301"})
        lines = table.find_all("dt")

        indicators_to_bring = ["EPS", "PER", "BPS", "PBR", "업종PER"]
        indicators = dict()
        for line in lines:
            indicator = line.text.split(" ")
            if indicator[0] in indicators_to_bring:
                indicators[indicator[0]] = float(indicator[1].replace(",", ""))

        company_indicator = CompanyIndicator()
        company_indicator.code = code
        company_indicator.date = date.today()
        company_indicator.eps = indicators["EPS"]
        company_indicator.per = indicators["PER"]
        company_indicator.iper = indicators["업종PER"]
        company_indicator.bps = indicators["BPS"]
        company_indicator.pbr = indicators["PBR"]
        company_indicator.save()

        return indicators

    def __get_price_info(self, price_data):
        """
        일간 정보를 딕셔너리로 생성: 종가, 시가, 고가, 저가, 거래량
        @return price_info: dict
        """
        price_info = dict()
        price_info["eps"] = price_data[1].text
        price_info["per"] = price_data[3].text
        price_info["bps"] = price_data[4].text
        price_info["pbr"] = price_data[5].text
        price_info["roe"] = price_data[6].text
        price_info["rob"] = price_data[6].text


class DailyPriceCrawler:

    def get_daily_prices_of_company(self, code: str, start_dt_str: str, end_dt_str: str):

        start_dt = datetime.strptime(start_dt_str, "%Y.%m.%d")
        end_dt = datetime.strptime(end_dt_str, "%Y.%m.%d")

        tmp_daily_prices = list()
        page = 0
        while True:
            page += 1
            daily_prices_of_page = self.__get_daily_prices_of_page(code, page)
            tmp_daily_prices.extend(daily_prices_of_page)
            if start_dt >= daily_prices_of_page[-1].date:
                break

        daily_prices = []
        for daily_price in tmp_daily_prices:
            if start_dt <= daily_price.date <= end_dt:
                daily_prices.append(daily_price)

        CompanyDailyPrice.objects.bulk_create(daily_prices, ignore_conflicts=True)

        return daily_prices

    def __get_daily_prices_of_page(self, code, page):
        """
        종목코드의 n 페이지의 {"날짜": {가격 정보}} 조회
        @return daily_price_info: dict
        """
        params = dict()
        params["code"] = code
        params["page"] = str(page)

        url = get_url("item/sise_day", params)
        soup = get_soup(url)

        base_table = soup.find_all("tr")
        price_table = base_table[2:7] + base_table[10:-2]

        company_daily_prices = list()
        for daily_price_info in price_table:
            price_data = daily_price_info.find_all("span")
            date_str = price_data[0].text.replace(".", "")
            img = str(daily_price_info.find("img"))

            company_daily_price = self.__get_daily_price(price_data, code, date_str, img)
            company_daily_prices.append(company_daily_price)

        return company_daily_prices

    def __get_daily_price(self, price_data, code, date_str, img):
        """
        일간 정보를 딕셔너리로 생성: 종가, 시가, 고가, 저가, 거래량
        @return price_info: dict
        """
        daily_price = CompanyDailyPrice()

        daily_price.code = code
        daily_price.id = code + "-" + date_str
        daily_price.date = datetime.strptime(date_str, "%Y%m%d")

        daily_price.closing = int(price_data[1].text.replace(",", ""))
        daily_price.opening = int(price_data[3].text.replace(",", ""))
        daily_price.highest = int(price_data[4].text.replace(",", ""))
        daily_price.lowest = int(price_data[5].text.replace(",", ""))
        daily_price.volume = int(price_data[6].text.replace(",", ""))

        change_amount = self.__get_rate_sign(img) + re.sub("[\t\n]", "", price_data[2].text)
        daily_price.change_amount = int(change_amount.replace(",", ""))

        return daily_price

    def __get_rate_sign(self, img):
        """
        상승/하락 기호 표시
        @return sign: str
        """
        sign = ""
        if "ico_up" in img:
            sign = "+"
        elif "ico_down" in img:
            sign = "-"

        return sign


class CompanyCrawler:

    def crawl_companies(self, market: str):
        companies = []
        page = 0
        while True:
            page += 1
            companies_of_page = self.__crawl_companies_of_page(market, page)
            companies.extend(companies_of_page)
            if len(companies_of_page) == 0:
                break
        Company.objects.bulk_create(companies, ignore_conflicts=True)

        return companies

    def __crawl_companies_of_page(self, market, page):
        params = dict()
        if market == "kospi":
            params["sosok"] = "0"
        elif market == "kosdaq":
            params["sosok"] = "1"
        params["page"] = str(page)

        url = get_url("sise/sise_market_sum", params)
        print(url)

        soup = get_soup(url)
        table = soup.find("table", {"class": "type_2"})
        rows = table.find_all("tr")

        companies = []
        for row in rows:
            name = row.find("a", {"class": "tltle"})
            if name == None:
                continue
            else:
                company = Company()
                company.name = name.text
                company.code = name.get("href").replace("/item/main.nhn?code=", "")
                company.market = market.upper()
                companies.append(company)

        return companies
