from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.index),
    path("current", views.current, name="current"),
    path("daily", views.daily, name="daily"),
    path("pers", views.per, name="per"),
    path("summary", views.summary, name="summary")
]
