from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import DateTimeField
from datetime import datetime

class Stock(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    buyPrice = models.DecimalField(max_digits=19, decimal_places=10, default=0)
    added_at = models.DateTimeField(default=datetime.now())

    # def __str__(self):
    #     return self.ticker