from django.db import models


class Company(models.Model):
    symbol = models.CharField(db_column="symbol", primary_key=True, max_length=6)
    iex_id = models.CharField(db_column="iex_id", max_length=20)
    name = models.CharField(db_column="name", max_length=100)
    exchange = models.CharField(db_column="exchange", max_length=6)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "usa_company"


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
        db_table = "usa_daily_price"


class QuarteryIndicator(models.Model):
    id = models.CharField(db_column="id", primary_key=True, max_length=13)
    symbol = models.CharField(db_column="symbol", max_length=6)
    fiscal_year = models.CharField(db_column="fiscal_year", max_length=4)
    fiscal_quarter = models.CharField(db_column="fiscal_quarter", max_length=1)
    eps = models.FloatField(db_column="eps")
    bps = models.FloatField(db_column="bps")
    roe = models.FloatField(db_column="roe")
    roa = models.FloatField(db_column="roa")
    total_equity = models.BigIntegerField(db_column="total_equity")
    total_assets = models.BigIntegerField(db_column="total_assets")
    net_income = models.BigIntegerField(db_column="net_income")
    shares_issued = models.BigIntegerField(db_column="shares_issued")

    class Meta:
        db_table = "usa_quarterly_indicator"
