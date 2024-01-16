from django.db import models
from reader.models import ReaderAccount
from .constants import TRANSACTION_TYPE
# Create your models here.

class Transaction(models.Model):
    user = models.ForeignKey(ReaderAccount, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

