from django.urls import path

from . import views

app_name = "usa"

urlpatterns = [
    path("companies/list", views.companies, name="companies")
]
