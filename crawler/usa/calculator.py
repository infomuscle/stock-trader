import logging

from usa.models import DailyPrice

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class ChangePercentCalculator:
    def calculate_change_percent(self, symbols: list):

        total_length = len(symbols)
        result = dict()
        for i, symbol in enumerate(symbols):
            try:
                result[symbol] = self.__calculate_change_percent_by_symbols(symbol)
            except Exception as e:
                logger.error("SYMBOL: {symbol} ERROR: {error}".format(symbol=symbol, error=e))
                result[symbol] = False
            print("{progress} / {total_length}".format(progress=i + 1, total_length=total_length))

        return result

    def __calculate_change_percent_by_symbols(self, symbol: str):
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


class DailyIndicatorCalculator():
    def calculate_daily_indicator(self):
        return
