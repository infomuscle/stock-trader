import json

from django.http import HttpResponse
from rest_framework import viewsets

from gateway import crawler
from gateway.models import GatewayModel
from gateway.serializers import GatewaySerializer


class GatewayViewSet(viewsets.ModelViewSet):
    queryset = GatewayModel.objects.all()
    serializer_class = GatewaySerializer


def current(request):
    c_price = crawler.get_current_price("005930")
    return HttpResponse(c_price)


def daily(request):
    print("goodgood")
    prices = crawler.get_daily_prices_to_page("005930", 3)

    return HttpResponse(json.dumps(prices))
