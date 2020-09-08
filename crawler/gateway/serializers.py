from .models import Gateway
from rest_framework import serializers

class GatewaySerializer(serializers.HyperlinkedModelSerializer):
    class Test:
        model = Gateway
        fields = ('no', 'name', 'price')