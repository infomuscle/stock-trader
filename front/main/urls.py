from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.index),
    path('current', views.current, name='current'),
    path('daily', views.daily, name='daily'),
    path('per', views.per, name='per'),
    path('pers', views.pers, name='pers')
]
