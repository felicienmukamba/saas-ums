from decimal import Decimal

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Payment


@receiver(pre_save, sender=Payment)
def payment_pre_save(sender, instance, **kwargs):
    if instance.receipt_number:
        instance.receipt_number = instance.receipt_number.strip().upper()
    if instance.amount_paid is not None:
        instance.amount_paid = abs(Decimal(instance.amount_paid))

