import json
import logging

import FinanceDataReader as fdr
import requests

from usa import constants as consts
from usa.models import *

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class CompanyCrawler:
    def crawl_companies(self):

        dataframes = [fdr.StockListing('NASDAQ'), fdr.StockListing('NYSE'), fdr.StockListing('AMEX')]  # 3213 3100 286
        exchanges = ["NAS", "NYS", "USAMEX"]

        companies = []
        for ex, df in enumerate(dataframes):
            for idx, row in df.iterrows():
                try:
                    company = self.__get_companies(df, idx, exchanges[ex])
                    company.save()
                    companies.append(company)
                except Exception as e:
                    logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=df.loc[idx, "Symbol"], error=e))

        return companies

    def __get_companies(self, df, idx, exchange):
        company = Company()
        company.symbol = df.loc[idx, "Symbol"]
        company.name = df.loc[idx, "Name"]
        company.exchange = exchange
        return company

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

        return company


class DailyPriceCrawler:

    def crawl_daily_prices(self, symbols: list, start_date: str, end_date: str):
        start_date = "{year}-{month}-{day}".format(year=start_date[:4], month=start_date[4:6], day=start_date[6:])
        end_date = "{year}-{month}-{day}".format(year=end_date[:4], month=end_date[4:6], day=end_date[6:])

        daily_prices = []
        total_length = len(symbols)
        for i, symbol in enumerate(symbols):
            try:
                daily_prices.extend(self.__crawl_daily_prices_by_symbol(symbol, start_date, end_date))
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))
            # print("{progress} / {total}".format(progress=i, total=total_length))

        return daily_prices

    def __crawl_daily_prices_by_symbol(self, symbol: str, start_date: str, end_date: str):
        df_daily_prices = fdr.DataReader(symbol, start_date, end_date)

        daily_prices = []
        for date, row in df_daily_prices.iterrows():
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

    def calculate_change_percent(self, symbols: list):

        total_length = len(symbols)
        result = dict()
        for i, symbol in enumerate(symbols):
            try:
                result[symbol] = self.calculate_change_percent_by_symbols(symbol)
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))
                result[symbol] = False
            print("{progress} / {total_length}".format(progress=i + 1, total_length=total_length))

        return result

    def calculate_change_percent_by_symbols(self, symbol: str):
        """
        change_percent = ((today / yesterday) - 1) * 100
        AONE+, GB, HZAC+, IACA+, NSH+ -> float division by zero
        @param symbol:
        @return:
        """
        daily_prices = DailyPrice.objects.filter(symbol=symbol).order_by("-date")
        for i in range(len(daily_prices)):
            if i == len(daily_prices) - 1:
                daily_prices[i].change_percent = 0
            else:
                daily_prices[i].change_percent = ((daily_prices[i].close / daily_prices[i + 1].close) - 1) * 100
        DailyPrice.objects.bulk_update(daily_prices, fields=["change_percent"])

        return True


class QuarterlyIndicatorCrawler:
    def crawl_quarterly_indicator(self, symbols: list):
        response = ""
        for symbol in symbols:
            response = self.__crawl_quarterly_indicator_by_symbol(symbol)

        return response

    def __crawl_quarterly_indicator_by_symbol(self, symbol: str):
        # assets               338516000000
        # liabilities          248028000000
        # stockholdersequity    90488000000
        # commonstocksharesauthorized   12600000000
        # commonstocksharesissued       4443236000
        print(symbol)

        url = "https://financialmodelingprep.com/api/v3/financial-statement-full-as-reported/"
        url += symbol
        url += "?apikey=" + consts.FMP_KEY
        url += " &period=quarter"
        print(url)

        response = requests.get(url)
        print(type(response.text))
        print(response.text)

        return response.text
