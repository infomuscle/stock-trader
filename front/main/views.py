import requests
from django.http import HttpResponse


def index(request):
    return HttpResponse("Main Screen!")


def test(request):
    return HttpResponse("Test!")


def current(request):
    current_price = requests.get("http://127.0.0.1:8081/api/current")
    return HttpResponse(current_price)


def daily(request):
    daily_price = requests.get("http://127.0.0.1:8081/api/daily")
    return HttpResponse(daily_price)
