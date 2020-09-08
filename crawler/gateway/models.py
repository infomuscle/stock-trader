from django.db import models


class GatewayModel(models.Model):
    no = models.AutoField(db_column='NO', primary_key=True)
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)
    page = models.IntegerField(db_column='PAGE', blank=True, null=True)
