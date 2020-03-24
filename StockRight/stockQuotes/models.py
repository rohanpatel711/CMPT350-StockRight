from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Stock(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10)

    # For Admin purposes
    def __str__(self):
        return self.ticker