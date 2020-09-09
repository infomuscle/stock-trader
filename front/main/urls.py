from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('current', views.current),
    path('daily', views.daily)
]
