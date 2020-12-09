from django.core import serializers
from django.http import HttpResponse

from usa.crawler import *


def companies(request):
    companies = CompanyCrawler().crawl_companies()
    return HttpResponse(serializers.serialize("json", companies))


def daily_price(request):
    req_json = request.GET.dict()
    symbol = req_json.get("symbol")
    start_date = req_json.get("start_date")
    end_date = req_json.get("end_date")

    if symbol == "test":
        return HttpResponse("SUCCESS")

    symbols = __get_symbols(symbol)

    daily_prices = DailyPriceCrawler().crawl_daily_prices(symbols, start_date, end_date)
    return HttpResponse(serializers.serialize("json", daily_prices))


def quarterly_indicator(request):
    req_json = request.GET.dict()
    symbol = req_json.get("symbol")

    if symbol == "test":
        return HttpResponse("QUARTERLY INDICATOR USA")

    symbols = __get_symbols(symbol)

    responses = QuarterlyIndicatorCrawler().crawl_quarterly_indicator(symbols)

    return HttpResponse(responses)


def __get_symbols(symbol: str):
    symbols = []
    if symbol == "all":
        symbols.extend(list(Company.objects.filter(exchange__in=["NAS", "NYS", "USAMEX"]).order_by().values_list('symbol', flat=True)))
    else:
        symbols.append(symbol)

    return symbols
