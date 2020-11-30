from django.core import serializers
from django.http import HttpResponse

from gateway.crawler import *
from gateway.models import Company


def daily_price(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    start_dt = req_json.get("start_dt")
    end_dt = req_json.get("end_dt")
    if code == "test":
        return HttpResponse("SUCCESS")

    codes = []
    if code == "all":
        codes.extend(list(Company.objects.all().values_list('code', flat=True)))
    else:
        codes.append(code)

    daily_prices = DailyPriceCrawler().crawl_daily_prices(codes, start_dt, end_dt)
    return HttpResponse(serializers.serialize("json", daily_prices))


def daily_indicator(request):
    req_json = request.GET.dict()
    code = req_json.get("code")

    codes = []
    if code == "all":
        codes.extend(list(Company.objects.all().values_list('code', flat=True)))
    else:
        codes.append(code)

    indicators = DailyIndicatorCrawler().crawl_daily_indicators(codes)
    return HttpResponse(serializers.serialize("json", indicators))


def quarterly_indicator(request):
    req_json = request.GET.dict()
    code = req_json.get("code")

    codes = []
    if code == "all":
        codes.extend(list(Company.objects.all().values_list('code', flat=True)))
    else:
        codes.append(code)

    indicators = QuaterlyIndicatorCrawler().crawl_quarterly_indicators(codes)
    return HttpResponse("SUCCESS")


def companies(request):
    req_json = request.GET.dict()
    market = req_json.get("market")
    if market == "test":
        return HttpResponse("SUCCESS")

    markets = []
    if market == "all":
        markets.extend(["kospi", "kosdaq"])
    else:
        markets.append(market)

    companies = CompanyCrawler().crawl_companies(markets)
    return HttpResponse(serializers.serialize("json", companies))


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    c_price = CurrentPriceCrawler().get_current_price(code)
    return HttpResponse(c_price)


def dart_test(request):
    result = DartCrawler().dart_test()
    return HttpResponse(result)
