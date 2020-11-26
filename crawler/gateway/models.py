from django.db import models


# class GatewayModel(models.Model):
#     no = models.AutoField(db_column='NO', primary_key=True)
#     company = models.CharField(db_column='COMPANY', max_length=10, blank=True, null=True)
#     page = models.IntegerField(db_column='PAGE', blank=True, null=True)


class Company(models.Model):
    code = models.CharField(db_column='code', primary_key=True, max_length=6)
    name = models.CharField(db_column='name', max_length=30)
    starred = models.CharField(db_column='starred', max_length=1, default="N")

    class Meta:
        db_table = "company"


class CompanyDailyPrice(models.Model):
    code = models.CharField(db_column='code', primary_key=True, max_length=6)
    date = models.DateField(db_column='date')
    opening = models.IntegerField(db_column='opening')
    closing = models.IntegerField(db_column='closing')
    highest = models.IntegerField(db_column='highest')
    lowest = models.IntegerField(db_column='lowest')
    volume = models.IntegerField(db_column='volume')

    class Meta:
        db_table = "company_daily_price"
        unique_together = (("code", "date"),)
