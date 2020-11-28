from django.db import models


class Company(models.Model):
    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    name = models.CharField(db_column="name", max_length=30)
    market = models.CharField(db_column="market", max_length=10)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "company"


class DailyPrice(models.Model):
    id = models.CharField(db_column="id", primary_key=True, max_length=15)
    code = models.CharField(db_column="code", max_length=6)
    date = models.DateField(db_column="date")
    opening = models.IntegerField(db_column="opening")
    closing = models.IntegerField(db_column="closing")
    highest = models.IntegerField(db_column="highest")
    lowest = models.IntegerField(db_column="lowest")
    change_amount = models.IntegerField(db_column="change_amount")
    change_rate = models.FloatField(db_column="change_rate")
    volume = models.IntegerField(db_column="volume")

    class Meta:
        db_table = "company_daily_price"


class DailyIndicator(models.Model):
    id = models.CharField(db_column="id", primary_key=True, max_length=15)
    code = models.CharField(db_column="code", max_length=6)
    date = models.DateField(db_column="date")
    eps = models.FloatField(db_column="eps")
    per = models.FloatField(db_column="per")
    bps = models.FloatField(db_column="bps")
    pbr = models.FloatField(db_column="pbr")
    roe = models.FloatField(db_column="roe")
    roa = models.FloatField(db_column="roa")
    iper = models.FloatField(db_column="iper")

    class Meta:
        db_table = "company_indicator"
