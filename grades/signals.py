from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Grade


@receiver(pre_save, sender=Grade)
def grade_pre_save(sender, instance, **kwargs):
    if instance.score is not None:
        instance.score = max(0, min(instance.score, 100))

