from django.db import models


class User(models.Model):
    MALE = "M"
    FEMALE = "F"

    GENDER_CHOICE = [
        (MALE, "male"),
        (FEMALE, "female")
    ]

    name         = models.CharField(max_length=32)
    gender       = models.CharField(max_length=8, choices=GENDER_CHOICE)
    email        = models.CharField(max_length=64)
    phone_number = models.CharField(max_length=32)
    password     = models.CharField(max_length=128)
    birthday     = models.DateField()

    class Meta:
        db_table = "users"
