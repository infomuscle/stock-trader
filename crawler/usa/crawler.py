import json
import logging
from datetime import datetime, timedelta

import FinanceDataReader as fdr
import requests

from usa import constants as consts
from usa.models import *

logger = logging.getLogger()


class CompanyCrawler:
    def crawl_companies(self):

        nasdaq = fdr.StockListing('NASDAQ')  # 3210
        nyse = fdr.StockListing('NYSE')  # 3100
        amex = fdr.StockListing('AMEX')  # 286

        companies = []

        return companies

    def crawl_companies_iex(self):
        url = consts.URL_BODY_IEX + "/ref-data/symbols"
        url += "?token=" + consts.IEX_KEYS
        companies_json = json.loads(requests.get(url).text)

        companies = []
        for company_json in companies_json:
            company = self.__get_company(company_json)
            company.save()
            companies.append(company)

        return companies

    def __get_company(self, company_json):
        company = Company()
        company.symbol = company_json["symbol"]
        company.iex_id = company_json["iexId"]
        company.name = company_json["name"]
        company.exchange = company_json["exchange"]
        if company_json["isEnabled"] == False:
            company.enabled = "N"

        return company


class DailyPriceCrawler:

    def crawl_daily_prices(self, symbols, start_date, end_date):

        start_date = start_date[:4] + "-" + start_date[4:6] + "-" + start_date[6:]
        end_date = end_date[:4] + "-" + end_date[4:6] + "-" + end_date[6:]

        daily_prices = []
        for symbol in symbols:
            daily_prices.extend(self.__crawl_daily_prices_by_symbol(symbol, start_date, end_date))

        return daily_prices

    def __crawl_daily_prices_by_symbol(self, symbol, start_date, end_date):

        df_daily_prices = fdr.DataReader(symbol, start_date, end_date)

        daily_prices = []
        for date in df_daily_prices.iterrows():
            daily_price = DailyPrice()
            daily_price.id = "{symbol}-{date}".format(symbol=symbol, date=str(date).split(" ")[0].replace("-", ""))
            daily_price.symbol = symbol
            daily_price.date = date
            daily_price.close = df_daily_prices.loc[date, "Close"]
            daily_price.open = df_daily_prices.loc[date, "Open"]
            daily_price.high = df_daily_prices.loc[date, "High"]
            daily_price.low = df_daily_prices.loc[date, "Low"]
            daily_price.volume = df_daily_prices.loc[date, "Volume"]
            daily_price.change = df_daily_prices.loc[date, "Change"]
            daily_price.save()
            daily_prices.append(daily_price)

        return daily_prices

    def crawl_daily_prices_iex(self, symbols, start_date_str, end_date_str):

        start_date = datetime.strptime(start_date_str, "%Y%m%d")
        end_date = datetime.strptime(end_date_str, "%Y%m%d")

        daily_prices = []
        for symbol in symbols:
            daily_prices.extend(self.__crawl_daily_prices_of_range_iex(symbol, start_date, end_date))

        return daily_prices

    def __crawl_daily_prices_of_range_iex(self, symbol, start_date, end_date):

        search_date = start_date
        daily_prices = []
        while search_date <= end_date:
            try:
                daily_prices.extend(self.__crawl_daily_price_by_symbol_iex(symbol, search_date))
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))
            search_date += timedelta(days=1)

        return daily_prices

    def __crawl_daily_price_by_symbol_iex(self, symbol, date):
        url = consts.URL_BODY_IEX + "/stock/{symbol}/chart/date/{date}".format(symbol=symbol, date=date.strftime("%Y%m%d"))
        url += "?token=" + consts.IEX_KEYS
        url += "&chartByDay=" + "true"
        url += "&changeFromClose=" + "true"

        response = requests.get(url).text
        print(response)
        daily_prices_json = json.loads(response)

        daily_prices = []
        for daily_price_json in daily_prices_json:
            daily_price = self.__get_daily_price_iex(daily_price_json)
            daily_price.save()
            daily_prices.append(daily_price)

        return daily_prices

    def __get_daily_price_iex(self, daily_price_json):
        daily_price = DailyPrice()
        daily_price.id = "{symbol}-{date}".format(symbol=daily_price_json["symbol"], date=daily_price_json["date"].replace("-", ""))
        daily_price.symbol = daily_price_json["symbol"]
        daily_price.date = datetime.strptime(daily_price_json["date"], "%Y-%m-%d")
        daily_price.close = daily_price_json["close"]
        daily_price.open = daily_price_json["open"]
        daily_price.high = daily_price_json["high"]
        daily_price.low = daily_price_json["low"]
        daily_price.change = daily_price_json["change"]
        daily_price.change_percent = daily_price_json["changePercent"]
        daily_price.volume = daily_price_json["volume"]

        return daily_price


class QuarterlyIndicatorCrawler:
    def crawl_quarterly_indicator(self, symbols):
        quarterly_indicators = []
        for symbol in symbols:
            quarterly_indicators.extend(self.__crawl_quarterly_indicator_by_symbol(symbol))

        return quarterly_indicators

    def __crawl_quarterly_indicator_by_symbol(self, symbol):
        url = consts.URL_BODY_IEX + "/time-series/fundamentals/{symbol}/{period}".format(symbol=symbol, period="quarterly")
        url += "?token=" + consts.IEX_KEYS

        response = requests.get(url).text
        fundamentals_json = json.loads(response)

        quarterly_indicators = []
        for fundamental_json in fundamentals_json:
            quarterly_indicator = self.__get_quarterly_indicator(symbol, fundamental_json)
            quarterly_indicator.save()
            quarterly_indicators.append(quarterly_indicator)

        return quarterly_indicators

    def __get_quarterly_indicator(self, symbol, fundamental_json):
        quarterly_indicator = QuarteryIndicator()

        keys = [symbol, fundamental_json["fiscalYear"], fundamental_json["fiscalQuarter"]]
        quarterly_indicator.id = "{symbol}-{fiscal_year}-{fiscal_quarter}".format(symbol=keys[0], fiscal_year=keys[1], fiscal_quarter=keys[2])
        quarterly_indicator.symbol = keys[0]
        quarterly_indicator.fiscal_year = keys[1]
        quarterly_indicator.fiscal_quarter = keys[2]

        quarterly_indicator.total_assets = fundamental_json["assetsUnadjusted"]
        quarterly_indicator.total_equity = fundamental_json["assetsUnadjusted"]
        quarterly_indicator.net_income = fundamental_json["incomeNet"]
        quarterly_indicator.shares_issued = fundamental_json["sharesIssued"]

        quarterly_indicator.eps = quarterly_indicator.net_income / quarterly_indicator.shares_issued
        quarterly_indicator.bps = quarterly_indicator.total_assets / quarterly_indicator.shares_issued
        quarterly_indicator.roe = (quarterly_indicator.net_income / quarterly_indicator.total_equity) * 100
        quarterly_indicator.roa = (quarterly_indicator.net_income / quarterly_indicator.total_assets) * 100

        return quarterly_indicator
