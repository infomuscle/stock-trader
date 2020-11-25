from django.conf.urls import url, include
from rest_framework import routers

from gateway import views

app_name = 'gateway'

router = routers.DefaultRouter()
router.register('gateway', views.GatewayViewSet)
urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api/daily', views.daily),
    url(r'^api/current', views.current),
    url(r'^api/per', views.per),
    url(r'^api/indicators', views.indicators),
    url(r'^api/companies/list', views.companies),
    url(r'^api/companies/name', views.name),
    url(r'^api/companies/code', views.code),
    url(r'^api/test/g', views.test_get),
    url(r'^api/test/p', views.test_post)
]
