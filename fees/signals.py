from decimal import Decimal

from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import AcademicFee


@receiver(pre_save, sender=AcademicFee)
def academic_fee_pre_save(sender, instance, **kwargs):
    if instance.amount is not None:
        instance.amount = abs(Decimal(instance.amount))

