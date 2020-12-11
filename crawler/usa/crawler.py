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


class QuarterlyIndicatorCrawler:
    """
    SYMBOL: NKTX ERROR: unsupported operand type(s) for /: 'float' and 'NoneType'
    SYMBOL: NNA ERROR: unsupported operand type(s) for /: 'float' and 'NoneType'
    SYMBOL: NMI ERROR: '04'
    SYMBOL: ABM ERROR: '07'
    SYMBOL: NLSP ERROR: '01'
    SYMBOL: ABG ERROR: float division by zero
    SYMBOL: ABCM ERROR: '01'
    []
    """

    def crawl_quarterly_indicator(self, symbols: list):

        quarterly_indicators = list()
        for symbol in symbols:
            try:
                quarterly_indicators.extend(self.__crawl_quarterly_indicator_by_symbol(symbol))
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))

        return quarterly_indicators

    def __crawl_quarterly_indicator_by_symbol(self, symbol: str):
        income_statements = self.__crawl_income_statement_by_symbol(symbol)
        balance_sheets = self.__crawl_balance_sheet_by_symbol(symbol)

        combined = dict()
        for id in income_statements:
            if id not in combined:
                combined[id] = dict()
            combined[id]["netIncome"] = income_statements[id].get("netIncome")
            combined[id]["eps"] = income_statements[id].get("eps")

        for id in balance_sheets:
            if id not in combined:
                combined[id] = dict()
            combined[id]["totalAssets"] = balance_sheets[id].get("totalAssets")
            combined[id]["totalEquity"] = balance_sheets[id].get("totalEquity")
            combined[id]["sharesIssued"] = balance_sheets[id].get("sharesIssued")

        quarterly_indicators = list()
        for id in combined:
            try:
                quarterly_indicator = QuarterlyIndicator()
                quarterly_indicator.id = id

                id_splits = id.split("-")
                quarterly_indicator.symbol = id_splits[0]
                quarterly_indicator.fiscal_year = id_splits[1]
                quarterly_indicator.fiscal_quarter = id_splits[2]

                quarterly_indicator.total_assets = combined[id].get("totalAssets")
                quarterly_indicator.total_equity = combined[id].get("totalEquity")
                quarterly_indicator.shares_issued = combined[id].get("sharesIssued")
                quarterly_indicator.net_income = combined[id].get("netIncome")

                quarterly_indicator.eps = quarterly_indicator.net_income / quarterly_indicator.shares_issued
                quarterly_indicator.bps = quarterly_indicator.total_assets / quarterly_indicator.shares_issued
                quarterly_indicator.roe = (quarterly_indicator.net_income / quarterly_indicator.total_equity) * 100
                quarterly_indicator.roa = (quarterly_indicator.net_income / quarterly_indicator.total_assets) * 100

                quarterly_indicator.save()
                quarterly_indicators.append(quarterly_indicator)
            except Exception as e:
                logger.error("ID: {id} ERROR: {error}".format(id=id, error=e))

        return quarterly_indicators

    def __crawl_income_statement_by_symbol(self, symbol: str):
        url = "{fmp_url_body}/income-statement/{symbol}?apikey={key}&period=quarter&limit=5".format(fmp_url_body=consts.FMP_URL_BODY, symbol=symbol, key=consts.FMP_KEY)

        response = requests.get(url)
        income_statements = json.loads(response.text)
        print(json.dumps(income_statements))

        is_simple = dict()
        for income_statement in income_statements:
            temp = dict()
            temp["netIncome"] = income_statement.get("netIncome")
            temp["eps"] = income_statement.get("eps")

            date_splits = income_statement.get("date").split("-")
            id = "{symbol}-{fiscalYear}-{quarter}".format(symbol=income_statement.get("symbol"), fiscalYear=date_splits[0], quarter=consts.QUATER_MAPPER[date_splits[1]])
            is_simple[id] = temp

        return is_simple

    def __crawl_balance_sheet_by_symbol(self, symbol: str):
        url = "{fmp_url_body}/balance-sheet-statement/{symbol}?apikey={key}&period=quarter&limit=5".format(fmp_url_body=consts.FMP_URL_BODY, symbol=symbol, key=consts.FMP_KEY)

        response = requests.get(url)
        balance_sheets = json.loads(response.text)
        print(json.dumps(balance_sheets))

        bs_simple = dict()
        for balance_sheet in balance_sheets:
            temp = dict()
            temp["totalAssets"] = balance_sheet.get("totalAssets")
            temp["totalEquity"] = balance_sheet.get("totalStockholdersEquity")
            temp["sharesIssued"] = balance_sheet.get("commonStock")

            date_splits = balance_sheet.get("date").split("-")
            id = "{symbol}-{fiscalYear}-{quarter}".format(symbol=balance_sheet.get("symbol"), fiscalYear=date_splits[0], quarter=consts.QUATER_MAPPER[date_splits[1]])
            bs_simple[id] = temp

        return bs_simple
