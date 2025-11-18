from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import CourseAssignment


@receiver(pre_save, sender=CourseAssignment)
def assignment_pre_save(sender, instance, **kwargs):
    if instance.assignment_role:
        instance.assignment_role = instance.assignment_role.strip().title()

