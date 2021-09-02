from django.db import models


class User(models.Model):
    name         = models.CharField(max_length=32)
    gender       = models.CharField(max_length=8)
    email        = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    password     = models.CharField(max_length=128)
    birthday     = models.DateField()

    class Meta:
        db_table = "users"