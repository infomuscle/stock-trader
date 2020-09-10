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
    url(r'^api/tickers', views.tickers),
    url(r'^api/test/g', views.test_get),
    url(r'^api/test/p', views.test_post)
]
print(urlpatterns)
