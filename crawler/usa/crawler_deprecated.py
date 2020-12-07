import json
import logging
from datetime import datetime, timedelta

import requests

from kor.models import DailyPrice

logger = logging.getLogger()


class DailyPriceCrawler:
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

    def __crawl_daily_price_by_symbol_iex(self, symbol, date, consts=None):
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
