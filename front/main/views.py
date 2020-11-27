from django.shortcuts import render

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
    return render(request, 'main/price.html', context)


def indicator(request):
    context = {}
    return render(request, 'main/indicator.html', context)


def crawl(request):
    context = {}
    return render(request, 'main/crawl.html', context)


def trade(request):
    context = {}
    return render(request, 'main/trade.html', context)
