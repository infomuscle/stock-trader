import json

import requests
from main import constants as consts
from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def crawl(request):
    context = {}
    return render(request, 'main/crawl.html', context)

def companies(request):
    context = {}
    return render(request, 'main/companies.html', context)


def current(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/current"
    # url += '?code=' + code
    url += '?code=' + consts.CODE_SAMSUNG_ELECTRONICS
    current_price = requests.get(url)

    context = {}
    return render(request, 'main/current.html', context)


def daily(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/daily"
    url += '?code=' + code
    daily_price = requests.get(url)

    context = {}
    return render(request, 'main/daily.html', context)


# def per_deprecated(request):
#     req_json = request.GET.dict()
#     code = req_json.get("code")
#     url = consts.URL_BODY_CRAWLER + "/api/per"
#     url += '?code=' + code
#     per = requests.get(url)
#     return HttpResponse(per)


#
# def per(request):
#     url_tickers = consts.URL_BODY_CRAWLER + "/api/companies/list"
#     res_tickers = requests.get(url_tickers)
#     tickers = json.loads(res_tickers.content)
#
#     pers = dict()
#     for i, ticker in enumerate(tickers):
#         if i == 10:
#             break
#         url_per = consts.URL_BODY_CRAWLER + "/api/per"
#         url_per += "?code=" + ticker["code"]
#         res_per = requests.get(url_per)
#         pers[ticker["name"]] = res_per.text
#
#     context = {}
#     return render(request, 'main/per.html', context)


def summary(request):
    context = {}
    return render(request, 'main/summary.html', context)
