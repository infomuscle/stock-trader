import requests
from django.http import HttpResponse
from django.shortcuts import render

import main.constants as consts
from main.models import *


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def companies(request):
    context = {}

    companies = Company.objects.all()
    context["companies"] = companies

    return render(request, 'main/companies.html', context)


def summary(request):
    context = {}

    return render(request, 'main/summary.html', context)


def price(request):
    context = {}

    prices = DailyPrice.objects.all()
    context["prices"] = prices

    return render(request, 'main/price.html', context)


def indicator(request):
    context = {}

    indicators = DailyIndicator.objects.all()
    context["indicators"] = indicators

    return render(request, 'main/indicator.html', context)


def crawl(request):
    context = {}
    return render(request, 'main/crawl.html', context)


def crawl_daily_price(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    start_dt = req_json.get("start_dt")
    end_dt = req_json.get("end_dt")

    url = consts.URL_BODY_CRAWLER + "/api/daily/price"
    url += '?code=' + code
    url += '&start_dt=' + start_dt
    url += '&end_dt=' + end_dt

    response = requests.get(url)
    return HttpResponse(response.text)


def crawl_daily_indicator(request):
    req_json = request.GET.dict()
    code = req_json.get("code")

    url = consts.URL_BODY_CRAWLER + "/api/daily/indicator"
    url += '?code=' + code

    response = requests.get(url)
    return HttpResponse(response.text)


def crawl_company(request):
    req_json = request.GET.dict()
    market = req_json.get("market")
    url = consts.URL_BODY_CRAWLER + "/api/companies/list"
    url += "?market=" + market
    print(url)

    response = requests.get(url)
    return HttpResponse(response.text)


def trade(request):
    context = {}
    return render(request, 'main/trade.html', context)
