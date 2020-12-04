from django.urls import path

from . import views

app_name = "kor"

urlpatterns = [
    path('daily/price', views.daily_price, name="daily_price"),
    path('daily/indicator', views.daily_indicator, name="daily_indicator"),

    path('quarterly/indicator', views.quarterly_indicator, name="quarterly_indicator"),

    path('companies/list', views.companies, name="companies"),

    path('current', views.current, name="current"),

    path('test', views.test, name="test")
    # path('/daily/(?P<date>.+)/price', views.daily),
]
