from django.test import TestCase

from gateway.crawler import *


class CrawlerTestCase(TestCase):
    def test_daily_price_crawler(self):
        daily_price_crawler = DailyPriceCrawler()
        print("TEST")

        code = "005930"
        start_dt = "2020.11.01"
        end_dt = "2020.11.27"
        daily_prices = daily_price_crawler.get_daily_prices_of_company(code, start_dt, end_dt)
        print(daily_prices)

