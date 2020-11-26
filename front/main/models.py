from django.db import models


# Create your models here.
class Company(models.Model):
    code = models.CharField(db_column="code", primary_key=True, max_length=6)
    name = models.CharField(db_column="name", max_length=30)
    starred = models.CharField(db_column="starred", max_length=1, default="N")

    class Meta:
        db_table = "company"
