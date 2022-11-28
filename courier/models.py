from django.db import models


class Courier(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    def __str__(self) -> str:
        return '{} {}'.format(self.first_name, self.last_name)