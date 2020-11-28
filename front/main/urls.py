from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index, name="index"),

    path("companies", views.companies, name="companies"),
    path("summary", views.summary, name="summary"),
    path("price", views.price, name="price"),
    path("indicator", views.indicator, name="indicator"),

    path("crawl", views.crawl, name="crawl"),
    path("crawl_daily_price", views.crawl_daily_price, name="crawl_daily_price"),
    path("crawl_daily_indicator", views.crawl_daily_indicator, name="crawl_daily_indicator"),
    path("crawl_company", views.crawl_company, name="crawl_company"),

    path("trade", views.trade, name="trade")
]
