from django.db import models


class Company(models.Model):
    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    name = models.CharField(db_column="name", max_length=30)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "company"


class CompanyDailyPrice(models.Model):
    class Meta:
        db_table = "company_daily_price"
        # unique_together = (("code", "date"),)
        # constraints = [
        models.UniqueConstraint(fields=['code', 'date'], name='company_daily_price_pk')
        # ]

    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    date = models.DateField(db_column="date")
    opening = models.IntegerField(db_column="opening")
    closing = models.IntegerField(db_column="closing")
    highest = models.IntegerField(db_column="highest")
    lowest = models.IntegerField(db_column="lowest")
    volume = models.IntegerField(db_column="volume")


class CompanyIndicator(models.Model):
    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    date = models.DateField(db_column="date")
    eps = models.FloatField(db_column="eps")
    per = models.FloatField(db_column="per")
    bps = models.FloatField(db_column="bps")
    pbr = models.FloatField(db_column="pbr")
    roe = models.FloatField(db_column="roe")
    roa = models.FloatField(db_column="roa")

    class Meta:
        db_table = "company_indicator"
        unique_together = (("code", "date"),)
