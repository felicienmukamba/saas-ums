from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import AcademicYear, Department, Faculty, Semester


def _normalize_code(instance):
    if hasattr(instance, "code") and instance.code:
        instance.code = instance.code.strip().upper()


@receiver(pre_save, sender=AcademicYear)
def academic_year_pre_save(sender, instance, **kwargs):
    _normalize_code(instance)


@receiver(pre_save, sender=Semester)
def semester_pre_save(sender, instance, **kwargs):
    _normalize_code(instance)


@receiver(pre_save, sender=Faculty)
def faculty_pre_save(sender, instance, **kwargs):
    _normalize_code(instance)
    if instance.name:
        instance.name = instance.name.strip()


@receiver(pre_save, sender=Department)
def department_pre_save(sender, instance, **kwargs):
    _normalize_code(instance)
    if instance.name:
        instance.name = instance.name.strip()

