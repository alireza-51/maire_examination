from django.db import models


class Courier(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)