import json

from django.core import serializers
from django.http import HttpResponse

from gateway import crawler


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    c_price = crawler.get_current_price(code)
    return HttpResponse(c_price)


def daily_price(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    start_dt = req_json.get("start_dt")
    end_dt = req_json.get("end_dt")

    daily_crawler = crawler.DailyPriceCrawler()
    prices = daily_crawler.get_daily_prices_of_company(code, start_dt, end_dt)

    return HttpResponse(serializers.serialize("json", prices))


def daily_indicator(request):
    # 수정 필요
    req_json = request.GET.dict()
    code = req_json.get("code")
    date = req_json.get("date")

    daily_crawler = crawler.DailyPriceCrawler()
    # prices = daily_crawler.get_daily_prices_to_page(code, 5)
    return HttpResponse("success")
    # return HttpResponse(json.dumps(prices))


def indicators(request):
    req_json = request.GET.dict()
    code = req_json.get("code")

    company_detail_crawler = crawler.CompanyDetailCrawler()
    indicators = company_detail_crawler.get_indicators(code)

    return HttpResponse(str(indicators))


def companies(request):
    req_json = request.GET.dict()
    type = req_json.get("type")
    krs_companies_crawler = crawler.KrxCompaniesCrawler()
    companies_str = krs_companies_crawler.get_companies(type)
    return HttpResponse(companies_str)


def name(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    krs_companies_crawler = crawler.KrxCompaniesCrawler()
    code_name = krs_companies_crawler.get_code_name()
    name = code_name[code]
    return HttpResponse(name)


def code(request):
    req_json = request.GET.dict()
    name = req_json.get("name")
    krs_companies_crawler = crawler.KrxCompaniesCrawler()
    name_code = krs_companies_crawler.get_name_code()
    code = name_code[name]
    return HttpResponse(code)


def test_get(request):
    req_dict = request.GET.dict()
    return HttpResponse(str(req_dict))


def test_post(request):
    req_dict = json.loads(request.body)
    return HttpResponse(str(req_dict))
