import requests
from django.shortcuts import render

from main import constants as consts
from main.models import *


def index(request):
    context = {}
    return render(request, 'main/index.html', context)


def crawl(request):
    context = {}
    return render(request, 'main/crawl.html', context)


def companies(request):
    context = {}

    companies = Company.objects.all()
    context["companies"] = companies

    return render(request, 'main/companies.html', context)


def price(request):
    context = {}
    return render(request, 'main/price.html', context)


def indicator(request):
    context = {}
    return render(request, 'main/indicator.html', context)


def daily(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    url = consts.URL_BODY_CRAWLER + "/api/daily"
    url += '?code=' + code
    daily_price = requests.get(url)

    context = {}
    return render(request, 'main/daily.html', context)


def summary(request):
    context = {}
    return render(request, 'main/summary.html', context)
