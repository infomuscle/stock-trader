import json
import logging
from datetime import datetime

import requests

from usa import constants as consts
from usa.models import *

logger = logging.getLogger()


class CompanyCrawler:
    def crawl_companies(self):
        url = consts.URL_BODY_IEX + "/ref-data/symbols"
        url += "?token=" + consts.IEX_KEYS
        companies_json = json.loads(requests.get(url).text)

        companies = []
        for company_json in companies_json:
            company = Company()
            company.symbol = company_json["symbol"]
            company.iex_id = company_json["iexId"]
            company.name = company_json["name"]
            company.exchange = company_json["exchange"]
            company.save()
            companies.append(company)

        return companies


class DailyPriceCrawler:
    def crawl_daily_prices(self, symbols, range):

        daily_prices = []
        for symbol in symbols:
            daily_prices.extend(self.__crawl_daily_prices_by_symbol(symbol, range))

        return daily_prices

    def __crawl_daily_prices_by_symbol(self, symbol, range):
        url = consts.URL_BODY_IEX + "/stock/{symbol}/chart/{range}".format(symbol=symbol, range=range)
        url += "?token=" + consts.IEX_KEYS

        daily_prices = []

        try:
            response = requests.get(url).text
            daily_prices_json = json.loads(response)

            for daily_price_json in daily_prices_json:
                daily_price = self.__get_daily_price(daily_price_json)
                daily_price.save()
                daily_prices.append(daily_price)
        except Exception as e:
            logger.error(e)

        return daily_prices

    def __get_daily_price(self, daily_price_json):
        daily_price = DailyPrice()
        daily_price.id = daily_price_json["symbol"] + "-" + daily_price_json["date"].replace("-", "")
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
