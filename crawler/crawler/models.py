from django.db import models


class Company(models.Model):
    def __init__(self):
        super().__init__()

    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    name = models.CharField(db_column="name", max_length=30)
    market = models.CharField(db_column="market", max_length=10)
    starred = models.CharField(db_column="starred", max_length=1, default="N")
    corp_code = models.CharField(db_column="corp_code", max_length=8)

    class Meta:
        db_table = "company"


class DailyPrice(models.Model):
    def __init__(self):
        super().__init__()

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
        db_table = "daily_price"


class DailyIndicator(models.Model):
    def __init__(self):
        super().__init__()

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
        db_table = "daily_indicator"


class QuarterlyIndicator(models.Model):
    def __init__(self):
        super().__init__()

    # def __init__(self, balance_sheet):
    #     super().__init__()

    id = models.CharField(db_column="id", primary_key=True, max_length=15)
    code = models.CharField(db_column="code", max_length=6)
    quarter_start = models.DateField(db_column="quarter_start")
    quarter_end = models.DateField(db_column="quarter_end")
    eps = models.FloatField(db_column="eps")
    bps = models.FloatField(db_column="bps")
    roe = models.FloatField(db_column="roe")
    roa = models.FloatField(db_column="roa")
    net_income = models.IntegerField(db_column="net_income")
    net_worth = models.IntegerField(db_column="net_worth")
    stock_amount = models.IntegerField(db_column="stock_amount")
    total_equity = models.IntegerField(db_column="total_equity")
    total_assets = models.IntegerField(db_column="total_assets")


class BalanceSheet(models.Model):
    def __init__(self):
        super().__init__()

    id = models.CharField(primary_key=True, max_length=13)
    code = models.CharField(max_length=6)
    quarter_end = models.DateField()
    total_assets = models.IntegerField()
    total_liabilities = models.IntegerField()
    total_equity = models.IntegerField()


class IncomeStatement(models.Model):
    def __init__(self):
        super().__init__()

    id = models.CharField(primary_key=True, max_length=13)
    code = models.CharField(max_length=6)
    quarter_start = models.DateField()
    quarter_end = models.DateField()
    net_income = models.IntegerField()
