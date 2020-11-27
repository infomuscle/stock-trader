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
    path("trade", views.trade, name="trade")
]
