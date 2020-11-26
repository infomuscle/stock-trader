import logging
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

from gateway import constants as consts
from gateway.models import Company

logger = logging.getLogger()


def get_url(tab_name: str, params: dict):
    """
    네이버 증권 URI에 탭 이름과 파라미터를 붙어 네이버 증권 URL 생성
    @return url: str
    """
    url = consts.URL_BODY_NAVER
    url += "/" + tab_name + ".nhn"

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

    url = get_url("sise", params)
    soup = get_soup(url)

    current_price = soup.find("strong", {"id": "_nowVal"})

    return current_price.text


class CompanyDetailCrawler:
    def get_per(self, code: str):
        """
        종목코드의 현재 시점 PER 조회
        @return per: str
        """
        params = dict()
        params["code"] = code

        url = get_url("sise", params)
        soup = get_soup(url)
        print(soup)

        per = soup.find("span", {"id": "_sise_per"})
        per = re.sub("[\t\n]", "", per.text)

        return per

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
                indicators[indicator[0]] = indicator[1]

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

    def get_daily_prices_to_page(self, code, page):
        """
        종목코드의 1부터 n 페이지까지의 {"날짜": {가격 정보}} 모두 조회
        @return daily_price_infos: dict
        """
        daily_price_infos = dict()

        for p in range(1, int(page) + 1):
            daily_price_infos.update(self.__get_daily_prices_of_page(code, p))

        return daily_price_infos

    def __get_daily_prices_of_page(self, code, page):
        """
        종목코드의 n 페이지의 {"날짜": {가격 정보}} 조회
        @return daily_price_info: dict
        """
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

            price_info = self.__get_price_info(price_data)

            img = str(daily_price_info.find("img"))
            rate = self.__get_rate_sign(img) + re.sub("[\t\n]", "", price_data[2].text)
            price_info["rate"] = rate

            daily_price_infos[price_data[0].text] = price_info
            print(daily_price_infos)

        return daily_price_infos

    def __get_price_info(self, price_data):
        """
        일간 정보를 딕셔너리로 생성: 종가, 시가, 고가, 저가, 거래량
        @return price_info: dict
        """
        price_info = dict()
        price_info["closing"] = price_data[1].text
        price_info["opening"] = price_data[3].text
        price_info["highest"] = price_data[4].text
        price_info["lowest"] = price_data[5].text
        price_info["volume"] = price_data[6].text

        return price_info

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


class KrxCompaniesCrawler:

    def __init__(self):
        self.url_body_krx = consts.URL_BODY_KRX_COMPANIES
        self.cd_kospi = consts.KRX_SEARCH_TYPE_CD_KOSPI
        self.cd_listed = consts.KRX_SEARCH_TYPE_CD_LISTED

    def get_companies(self, type: str):
        """
        KRX에서 모든 회사명/종목코드 조회
        type 지정에 따라 코스피/상장사 조회 가능
        @return companies_info: json
        """
        url = self.url_body_krx + "&searchType=" + self.cd_kospi if type == "kospi" else self.cd_listed

        df_companies_info = self.__get_df_companies_info(url)

        companies_info = df_companies_info.to_json(force_ascii=False, orient="records")

        companies = []
        for i in df_companies_info.index:
            company = Company()
            company.code = df_companies_info.at[i, 'code']
            company.name = df_companies_info.at[i, 'name']
            print(company.code, company.name, company.starred)

        return companies_info

    def get_code_name(self):
        """
        {"종목코드": "회사명"} 포맷의 딕셔너리 생성
        @return code_name: dict
        """
        url = self.url_body_krx + "&searchType=" + self.cd_listed

        df_companies_info = self.__get_df_companies_info(url)

        code_name = dict()
        for i in df_companies_info.index:
            code_name[df_companies_info.at[i, 'code']] = df_companies_info.at[i, 'name']

        return code_name

    def get_name_code(self):
        """
        {"회사명": "종목코드"} 포맷의 딕셔너리 생성
        @return name_code: dict
        """
        url = self.url_body_krx + "&searchType=" + self.cd_listed

        df_companies_info = self.__get_df_companies_info(url)

        name_code = dict()
        for i in df_companies_info.index:
            name_code[df_companies_info.at[i, 'name']] = df_companies_info.at[i, 'code']

        return name_code

    def __get_df_companies_info(self, url):
        """
        KRX에서 기업 정보 조회하여 회사명/종목코드만 남긴 데이터 프레임 리턴
        @return df_companies_info: Dataframe
        """
        df_companies_info = pd.read_html(url, header=0)[0]
        df_companies_info = df_companies_info[["회사명", "종목코드"]]
        df_companies_info = df_companies_info.rename(columns={"회사명": "name", "종목코드": "code"})
        df_companies_info.code = df_companies_info.code.map("{:06d}".format)

        return df_companies_info
