from django.urls import path

from usa import views

app_name = "usa"

urlpatterns = [
    path("companies/list", views.companies, name="companies"),
    path('daily/price', views.daily_price, name="daily_price"),
    path('daily/price/percent', views.change_percent, name="change_percent"),
    path('quarterly/indicator', views.quarterly_indicator, name="quarterly_indicator"),

]
