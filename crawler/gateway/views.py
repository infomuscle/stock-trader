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
    req_json = request.GET.dict()
    code = req_json.get("code")
    c_price = crawler.get_current_price(code)
    return HttpResponse(c_price)


def daily(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    prices = crawler.get_daily_prices_to_page(code, 3)
    return HttpResponse(json.dumps(prices))


def name(request):
    req_json = request.GET.dict()
    code = req_json.get("code")
    code_name = crawler.get_name_code()
    name = code_name[code]
    return name


def code(request):
    req_json = request.GET.dict()
    name = req_json.get("name")
    name_code = crawler.get_name_code()
    code = name_code[name]
    return code


def codes(request):
    code_list = crawler.get_code_list()

    return code_list


def test_get(request):
    req_dict = request.GET.dict()
    return HttpResponse(str(req_dict))


def test_post(request):
    req_dict = json.loads(request.body)
    return HttpResponse(str(req_dict))
