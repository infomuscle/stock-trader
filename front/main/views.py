import json

import requests
from main import constants as consts
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/current"
    url += '?code=' + code
    current_price = requests.get(url)
    return HttpResponse(current_price)


def daily(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/daily"
    url += '?code=' + code
    daily_price = requests.get(url)
    return HttpResponse(daily_price)


def per(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/per"
    url += '?code=' + code
    per = requests.get(url)
    return HttpResponse(per)


def pers(request):
    url_tickers = consts.URL_BODY_CRAWLER + "/api/companies/list"
    res_tickers = requests.get(url_tickers)
    tickers = json.loads(res_tickers.content)

    pers = dict()
    for i, ticker in enumerate(tickers):
        if i == 10:
            break
        url_per = consts.URL_BODY_CRAWLER + "/api/per"
        url_per += "?code=" + ticker["code"]
        res_per = requests.get(url_per)
        pers[ticker["name"]] = res_per.text

    return HttpResponse(str(pers))
