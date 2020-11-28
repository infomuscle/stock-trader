import logging
import re
from datetime import date
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from gateway import constants as consts
from gateway.models import *

logger = logging.getLogger()


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

        DailyPrice.objects.bulk_create(daily_prices, ignore_conflicts=True)

        return daily_prices

    def __get_daily_prices_of_page(self, code, page):
        """
        종목코드의 n 페이지의 {"날짜": {가격 정보}} 조회
        @return daily_price_info: dict
        """
        url = self.__get_url_for_daily_price(code, page)
        soup = _get_soup(url)

        base_table = soup.find_all("tr")
        price_table = base_table[2:7] + base_table[10:-2]

        daily_prices = list()
        for daily_price_info in price_table:
            price_data = daily_price_info.find_all("span")
            date_str = price_data[0].text.replace(".", "")
            img = str(daily_price_info.find("img"))

            daily_price = self.__get_daily_price(price_data, code, date_str, img)
            daily_prices.append(daily_price)

        return daily_prices

    def __get_url_for_daily_price(self, code, page):
        params = dict()
        params["code"] = code
        params["page"] = str(page)

        url = _generate_url("item/sise_day", params)

        return url

    def __get_daily_price(self, price_data, code, date_str, img):
        """
        일간 정보를 딕셔너리로 생성: 종가, 시가, 고가, 저가, 거래량
        @return price_info: dict
        """
        daily_price = DailyPrice()

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


class DailyIndicatorCrawler:

    def crawl_daily_indicators(self, codes):
        indicators = []
        for code in codes:
            indicators.append(self.crawl_daily_indicators_of_company(code))

        return indicators

    def crawl_daily_indicators_of_company(self, code: str):
        daily_indicator = DailyIndicator()
        daily_indicator.code = code
        daily_indicator.date = date.today()
        daily_indicator.id = code + "-" + str(daily_indicator.date).replace("-", "")

        url = consts.URL_BODY_NAVER_REPORT + code
        soup = _get_soup(url)

        try:
            table = soup.find("td", {"class": "td0301"})
            lines = table.find_all("dt")
        except Exception as e:
            logger.error("code: %s error: %s" % (code, e))
            return daily_indicator

        indicators_dict = self.__get_indicators_dict(lines, code)
        daily_indicator.eps = indicators_dict.get("EPS", None)
        daily_indicator.per = indicators_dict.get("PER", None)
        daily_indicator.bps = indicators_dict.get("BPS", None)
        daily_indicator.pbr = indicators_dict.get("PBR", None)
        daily_indicator.iper = indicators_dict.get("업종PER", None)

        return daily_indicator

    def __get_indicators_dict(self, lines, code):
        indicators_dict = dict()
        for line in lines:
            indicator = line.text.split(" ")
            if indicator[0] in consts.INDICATORS:
                try:
                    indicators_dict[indicator[0]] = float(indicator[1].replace(",", ""))
                except ValueError as e:
                    logger.error("code: %s error: %s" % (code, e))
                    pass

        return indicators_dict


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

        url = self.__get_url_for_company(market, page)
        soup = _get_soup(url)

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

    def __get_url_for_company(self, market, page):
        params = dict()
        if market == "kospi":
            params["sosok"] = "0"
        elif market == "kosdaq":
            params["sosok"] = "1"
        params["page"] = str(page)

        url = _generate_url("sise/sise_market_sum", params)

        return url


class CurrentPriceCrawler:

    def get_current_price(self, code: str):
        """
        종목코드의 현재 가격 조회
        @return current_price: str
        """
        params = dict()
        params["code"] = code

        url = _generate_url("item/sise", params)
        soup = _get_soup(url)

        current_price = soup.find("strong", {"id": "_nowVal"})

        return current_price.text


def _generate_url(tab_name: str, params: dict):
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


def _get_soup(url):
    """
    User-Agent가 포함된 HTTP 헤더와 URL로 BeautifulSoup 생성
    @return soup: BeautifulSoup
    """
    headers = {"User-Agent": consts.HEADER_VALUE_USER_AGENT}
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup
