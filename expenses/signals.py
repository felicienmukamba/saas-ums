from decimal import Decimal

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Expense


@receiver(pre_save, sender=Expense)
def expense_pre_save(sender, instance, **kwargs):
    if instance.reference_number:
        instance.reference_number = instance.reference_number.strip().upper()
    if instance.amount is not None:
        instance.amount = abs(Decimal(instance.amount))

