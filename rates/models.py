from django.db import models


class Rate(models.Model):
    date = models.DateField()
    euro = models.CharField(max_length=20)
    real = models.CharField(max_length=20)
    yen = models.CharField(max_length=20)

    def __str__(self):
        return str(self.date)
