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

    def crawl_daily_prices(self, codes: list, start_dt_str: str, end_dt_str: str):
        """
        리스트의 각 종목코드 데이터 조회
        @param codes:
        @param start_dt_str:
        @param end_dt_str:
        @return:
        """
        start_dt = datetime.strptime(start_dt_str, "%Y.%m.%d")
        end_dt = datetime.strptime(end_dt_str, "%Y.%m.%d")

        daily_prices = []
        for code in codes:
            daily_prices.extend(self.__crawl_daily_prices_of_company(code, start_dt, end_dt))

        return daily_prices

    def __crawl_daily_prices_of_company(self, code: str, start_dt, end_dt):
        """
        종목코드의 데이터 리턴
        @param code:
        @param start_dt:
        @param end_dt:
        @return:
        """
        tmp_daily_prices = list()
        page = 0
        while True:
            page += 1
            daily_prices_of_page = self.__crawl_daily_prices_of_page(code, page)
            tmp_daily_prices.extend(daily_prices_of_page)
            if start_dt >= daily_prices_of_page[-1].date:
                break

        daily_prices = []
        for daily_price in tmp_daily_prices:
            if start_dt <= daily_price.date <= end_dt:
                daily_prices.append(daily_price)

        DailyPrice.objects.bulk_create(daily_prices, ignore_conflicts=True)

        return daily_prices

    def __crawl_daily_prices_of_page(self, code: str, page: int):
        """
        종목코드의 n 페이지의 데이터 조회
        @param code:
        @param page:
        @return:
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

    def __get_url_for_daily_price(self, code: str, page: int):
        """
        URL 생성
        @param code:
        @param page:
        @return:
        """
        params = dict()
        params["code"] = code
        params["page"] = str(page)

        url = _generate_url("item/sise_day", params)

        return url

    def __get_daily_price(self, price_data, code, date_str, img):
        """
        오브젝트에 데이터 저장: 종가, 시가, 고가, 저가, 거래량
        @param price_data:
        @param code:
        @param date_str:
        @param img:
        @return:
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
        @param img:
        @return:
        """
        sign = ""
        if "ico_up" in img:
            sign = "+"
        elif "ico_down" in img:
            sign = "-"

        return sign


class DailyIndicatorCrawler:

    def crawl_daily_indicators(self, codes: list):
        """
        리스트 내 각 종목코도의 일간 지표 크롤링
        @param codes:
        @return:
        """
        daily_indicators = []
        for i, code in enumerate(codes):
            daily_indicators.append(self.__crawl_daily_indicators_of_company(code))
            print("PROGRESS: %d / %d" % (i, len(codes)))
        DailyIndicator.objects.bulk_create(daily_indicators, ignore_conflicts=True)

        return daily_indicators

    def __crawl_daily_indicators_of_company(self, code: str):
        """
        종목 코드의 일간 지표 크롤링
        @param code:
        @return:
        """
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

    def __get_indicators_dict(self, lines, code: str):
        """
        크롤링한 각 라인에서 {"지표":"값"} 포맷의 딕셔너리 리턴
        @param lines:
        @param code:
        @return:
        """
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


class QuaterlyIndicatorCrawler:
    def crawl_quarterly_indicators(self, codes: list):
        quarterly_indicators = []
        for i, code in enumerate(codes):
            # daily_indicators.append(self.__crawl_daily_indicators_of_company(code))
            print("PROGRESS: %d / %d" % (i, len(codes)))
        DailyIndicator.objects.bulk_create(quarterly_indicators, ignore_conflicts=True)

        return quarterly_indicators


class CompanyCrawler:
    def crawl_companies(self, markets: list):
        """
        리스트 내 각 시장의 종목 데이터 크롤링
        @param markets:
        @return:
        """
        companies = []
        for market in markets:
            companies.extend(self.__crawl_companies_of_market(market))

    def __crawl_companies_of_market(self, market: str):
        """
        해당 시장의 종목 데이터 크롤링: 코드, 이름
        @param market:
        @return:
        """
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

    def __crawl_companies_of_page(self, market: str, page: int):
        """
        n 페이지의 종목 데이터 크롤링
        @param market:
        @param page:
        @return:
        """
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

    def __get_url_for_company(self, market: str, page: int):
        """
        URL 생성
        @param market:
        @param page:
        @return:
        """
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
        @param code:
        @return:
        """
        params = dict()
        params["code"] = code

        url = _generate_url("item/sise", params)
        soup = _get_soup(url)

        current_price = soup.find("strong", {"id": "_nowVal"})

        return current_price.text


def _generate_url(tab_name: str, params: dict):
    """
    네이버 증권 URL에 탭 이름과 파라미터를 붙어 네이버 증권 URL 생성
    @param tab_name:
    @param params:
    @return:
    """
    url = consts.URL_BODY_NAVER
    url += tab_name + ".nhn"

    if (len(params.keys()) > 0):
        for i, k in enumerate(params.keys()):
            url += "?" if i == 0 else "&"
            url += k + "=" + params[k]

    return url


def _get_soup(url: str):
    """
    User-Agent가 포함된 HTTP 헤더와 URL로 BeautifulSoup 생성
    @param url:
    @return:
    """
    headers = {"User-Agent": consts.HEADER_VALUE_USER_AGENT}
    html_doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_doc.content, "html.parser")

    return soup
