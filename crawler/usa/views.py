from django.core import serializers
from django.http import HttpResponse

from usa.crawler import *


def companies(request):
    companies = CompanyCrawler().crawl_companies()
    return HttpResponse(serializers.serialize("json", companies))


def daily_price(request):
    req_json = request.GET.dict()
    symbol = req_json.get("symbol")

    daily_prices = DailyPriceCrawler().crawl_daily_prices(symbol)

    return HttpResponse(serializers.serialize("json", daily_prices))
