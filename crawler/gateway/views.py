from rest_framework import viewsets

from gateway.models import GatewayModel
from gateway.serializers import GatewaySerializer


class GatewayView(viewsets.ModelViewSet):
    queryset = GatewayModel.objects.all()
    serializer_class = GatewaySerializer
