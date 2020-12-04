from django.urls import path

from usa import views

app_name = "usa"

urlpatterns = [
    path("companies/list", views.companies, name="companies"),
    path('daily/price', views.daily_price, name="daily_price"),

]
