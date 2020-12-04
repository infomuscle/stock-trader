from django.urls import path, include

urlpatterns = [
    path('api/kor/', include('kor.urls')),
    path('api/usa/', include('usa.urls'))
]
