from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Course, CourseOffering


@receiver(pre_save, sender=Course)
def course_pre_save(sender, instance, **kwargs):
    if instance.course_code:
        instance.course_code = instance.course_code.strip().upper()
    if instance.course_name:
        instance.course_name = instance.course_name.strip()


@receiver(pre_save, sender=CourseOffering)
def course_offering_pre_save(sender, instance, **kwargs):
    if instance.promotion_name:
        instance.promotion_name = instance.promotion_name.strip().title()

