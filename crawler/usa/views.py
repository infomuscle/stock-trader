import json

from django.core import serializers
from django.http import HttpResponse

from usa.crawler import *


def companies(request):
    companies = CompanyCrawler().crawl_companies()
    return HttpResponse(serializers.serialize("json", companies))

