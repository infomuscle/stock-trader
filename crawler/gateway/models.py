from django.db import models


class GatewayModel(models.Model):
    no = models.AutoField(db_column='NO', primary_key=True)
    company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)
    page = models.IntegerField(db_column='PAGE', blank=True, null=True)


class Company(models.Model):
    company_code = models.CharField(db_column='COMPANY_CODE', primary_key=True)
    company_name = models.CharField(db_column='COMPANY_NAME')
    starred = models.CharField(db_column='STARRED')


class DailyInfoForCompany(models.Model):
    company_code = models.CharField(db_column='COMPANY_CODE', primary_key=True)
    date = models.DateField(db_column='DATE', primary_key=True)
    opening_price = models.IntegerField(db_column='OPENING_PRICE')
    closing_price = models.IntegerField(db_column='CLOSING_PRICE')
    highest_price = models.IntegerField(db_column='HIGHEST_PRICE')
    lowest_price = models.IntegerField(db_column='LOWEST_PRICE')
    volume = models.IntegerField(db_column='VOLUME')
    # per
    # market_capitalization
