# from django.conf.urls import url, include
# from rest_framework import routers
#
# from kor import views
#
# app_name = 'kor'
#
# router = routers.DefaultRouter()
# # router.register('kor', views.CrawlerViewSet)
# urlpatterns = [
#     url(r'^', include(router.urls)),
#     url(r'^api/daily/price', views.daily_price),
#     url(r'^api/daily/indicator', views.daily_indicator),
#
#     url(r'^api/quarterly/indicator', views.quarterly_indicator),
#
#     url(r'^api/companies/list', views.companies),
#
#     url(r'^api/current', views.current),
#
#     url(r'^api/test', views.test)
#     # url(r'^api/daily/(?P<date>.+)/price', views.daily),
# ]
from django.urls import path, include

urlpatterns = [
    # path('', include('kor.urls')),
    path('usa/', include('usa.urls'))
]