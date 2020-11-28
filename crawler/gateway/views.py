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

    codes = []
    if code == "all":
        codes.extend(list(Company.objects.all().values_list('code', flat=True)))
    else:
        codes.append(code)

    daily_price_crawler = crawler.DailyPriceCrawler()
    prices = []
    for code in codes:
        prices.extend(daily_price_crawler.get_daily_prices_of_company(code, start_dt, end_dt))

    return HttpResponse(serializers.serialize("json", prices))


def companies(request):
    req_json = request.GET.dict()
    market = req_json.get("market")

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


def daily_indicator(request):
    # 수정 필요
    req_json = request.GET.dict()
    code = req_json.get("code")
    date = req_json.get("date")

    daily_crawler = crawler.DailyPriceCrawler()
    # prices = daily_crawler.get_daily_prices_to_page(code, 5)
    return HttpResponse("success")
    # return HttpResponse(json.dumps(prices))


def test_get(request):
    req_dict = request.GET.dict()
    return HttpResponse(str(req_dict))


def test_post(request):
    req_dict = json.loads(request.body)
    return HttpResponse(str(req_dict))


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    c_price = crawler.get_current_price(code)
    return HttpResponse(c_price)
