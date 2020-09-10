import requests
from main import constants as consts
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def current(request):
    url = consts.URL_BODY_CRAWLER + "/api/current"
    url += '?code=' + consts.CODE_SAMSUNG_ELECTRONICS
    current_price = requests.get(url)
    return HttpResponse(current_price)


def daily(request):
    url = consts.URL_BODY_CRAWLER + "/api/daily"
    url += '?code=' + consts.CODE_SAMSUNG_ELECTRONICS
    daily_price = requests.get(url)
    return HttpResponse(daily_price)


def per(request):
    url = consts.URL_BODY_CRAWLER + "/api/per"
    url += '?code=' + consts.CODE_SAMSUNG_ELECTRONICS
    per = requests.get(url)
    return HttpResponse(per)


def pers(request):
    url_tickers = consts.URL_BODY_CRAWLER + "/api/tickers"
    tickers = requests.get(url_tickers)

    pers = dict()
    for t in tickers:
        url_pers = consts.URL_BODY_CRAWLER + "/api/per"
        url_pers += "?code=" + t["code"]
        per = requests.get(url_pers)
        pers[t["code"]] = per

    print(pers)
    return HttpResponse(pers)
