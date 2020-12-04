from django.db import models


class Company(models.Model):
    symbol = models.CharField(db_column="symbol", primary_key=True, max_length=6)
    iex_id = models.CharField(db_column="iex_id", max_length=20)
    name = models.CharField(db_column="name", max_length=100)
    exchange = models.CharField(db_column="exchange", max_length=6)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "company_usa"


class DailyPrice(models.Model):
    id = models.CharField(db_column="id", primary_key=True, max_length=15)
    symbol = models.CharField(db_column="symbol", max_length=6)
    date = models.DateField(db_column="date")
    open = models.FloatField(db_column="open")
    close = models.FloatField(db_column="close")
    high = models.FloatField(db_column="high")
    low = models.FloatField(db_column="low")
    change = models.FloatField(db_column="change")
    change_percent = models.FloatField(db_column="change_percent")
    volume = models.IntegerField(db_column="volume")

    class Meta:
        db_table = "daily_price_usa"
