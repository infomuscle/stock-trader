from django.urls import path

from . import views

app_name = "usa"

urlpatterns = [
    path("companies", views.companies, name="companies")

]
