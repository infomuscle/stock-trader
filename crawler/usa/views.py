from django.http import HttpResponse

from usa.crawler import *


def companies(request):
    result = SymbolCrawler().crawl_companies()
    return HttpResponse(result)
