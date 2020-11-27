from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.index),
    path("companies", views.companies, name="companies"),
    path("price", views.price, name="price"),
    path("indicator", views.indicator, name="indicator"),
    path("crawl", views.crawl, name="crawl"),
    path("trade", views.trade, name="trade"),
    path("daily", views.daily, name="daily"),
    path("summary", views.summary, name="summary")
]
