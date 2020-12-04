from django.db import models


class Company(models.Model):
    symbol = models.CharField(db_column="symbol", primary_key=True, max_length=6)
    iex_id = models.CharField(db_column="iex_id", max_length=20)
    name = models.CharField(db_column="name", max_length=100)
    exchange = models.CharField(db_column="exchange", max_length=6)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "company_usa"
