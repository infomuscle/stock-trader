import logging
import math

from usa.models import DailyPrice, DailyIndicator
from usa.models import QuarterlyIndicator

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ChangePercentCalculator:
    def calculate_change_percents(self, symbols: list):

        total_length = len(symbols)
        result = dict()
        for i, symbol in enumerate(symbols):
            try:
                result[symbol] = self.__calculate_change_percent_by_symbol(symbol)
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))
                result[symbol] = False
            print("{progress} / {total_length}".format(progress=i + 1, total_length=total_length))

        return result

    def __calculate_change_percent_by_symbol(self, symbol: str):
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


class DailyIndicatorCalculator:
    def calculate_daily_indicators(self, symbols: list):

        daily_indicators = list()
        for symbol in symbols:
            try:
                daily_indicators.extend(self.__calculate_daily_indicator_by_symbol(symbol))
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))

        return daily_indicators

    def __calculate_daily_indicator_by_symbol(self, symbol: str):
        daily_prices = DailyPrice.objects.filter(symbol=symbol)

        daily_indicators = list()
        for daily_price in daily_prices:
            try:
                quarter = "Q" + str(math.ceil(daily_price.date.month / 3))
                quarter_id = "{symbol}-{year}-{quarter}".format(symbol=symbol, year=daily_price.date.year, quarter=quarter)
                quarterly_indicator = QuarterlyIndicator.objects.get(id=quarter_id)

                daily_indicator = DailyIndicator()
                daily_indicator.id = daily_price.id
                daily_indicator.symbol = daily_price.symbol
                daily_indicator.date = daily_price.date

                daily_indicator.per = daily_price.close / quarterly_indicator.eps
                daily_indicator.pbr = daily_price.close / quarterly_indicator.bps

                daily_indicator.save()
                daily_indicators.append(daily_indicator)
            except Exception as e:
                logger.error("ID: {id} ERROR: {error}".format(id=id, error=e))

        return daily_indicators
