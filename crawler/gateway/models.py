from django.db import models


class GatewayModel(models.Model):
    no = models.AutoField(db_column='NO', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100)
    price = models.IntegerField(db_column='PRICE', blank=True, null=True)
