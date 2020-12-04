from django.urls import path, include
from rest_framework import routers

urlpatterns = [
    path('api/kor/', include('kor.urls')),
    path('api/usa/', include('usa.urls'))
]
