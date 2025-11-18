from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import AssessmentType, AssessmentWeighting


@receiver(pre_save, sender=AssessmentType)
def assessment_type_pre_save(sender, instance, **kwargs):
    if instance.name:
        instance.name = instance.name.strip().title()


@receiver(pre_save, sender=AssessmentWeighting)
def assessment_weighting_pre_save(sender, instance, **kwargs):
    if instance.weight_percentage is not None:
        instance.weight_percentage = max(0, min(instance.weight_percentage, 100))

