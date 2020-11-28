import json

from django.core import serializers
from django.http import HttpResponse

from gateway import crawler
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

    daily_price_crawler = crawler.DailyPriceCrawler()
    daily_prices = daily_price_crawler.crawl_daily_prices(codes, start_dt, end_dt)

    return HttpResponse(serializers.serialize("json", daily_prices))


def daily_indicator(request):
    req_json = request.GET.dict()
    code = req_json.get("code")

    codes = []
    if code == "all":
        codes.extend(list(Company.objects.all().values_list('code', flat=True)))
    else:
        codes.append(code)

    daily_indicator_crawler = crawler.DailyIndicatorCrawler()
    indicators = daily_indicator_crawler.crawl_daily_indicators(codes)

    return HttpResponse(serializers.serialize("json", indicators))


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

    companies_crawler = crawler.CompanyCrawler()
    companies = []
    for market in markets:
        companies.extend(companies_crawler.crawl_companies(market))
    return HttpResponse(serializers.serialize("json", companies))


def test_get(request):
    req_dict = request.GET.dict()
    return HttpResponse(str(req_dict))


def test_post(request):
    req_dict = json.loads(request.body)
    return HttpResponse(str(req_dict))


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    current_price_crawler = crawler.CurrentPriceCrawler()
    c_price = current_price_crawler.get_current_price(code)
    return HttpResponse(c_price)
