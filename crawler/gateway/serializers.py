from rest_framework import serializers

from .models import GatewayModel


class GatewaySerializer(serializers.HyperlinkedModelSerializer):
    class Crawl:
        model = GatewayModel
        fields = ('no', 'name', 'price')
