from rest_framework import viewsets

from gateway.models import Gateway
from gateway.serializers import GatewaySerializer


class Gateway(viewsets.ModelViewSet):
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer
