from django.test import TestCase
from gateway.crawler import *

class CrawlerTestCase(TestCase):
    def test_daily_price_crawler(self):

        daily_price_crawler= DailyPriceCrawler()
        print("TEST")

        # self.assertTrue(len(g.lottos) > 20) #성공실패 테스트 루틴은 assert 메소드를 사용한다.