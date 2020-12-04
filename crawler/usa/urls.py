from django.urls import path

from usa import views

app_name = "usa"

urlpatterns = [
    path("companies/list", views.companies, name="companies")
]
