from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Student, StudentSponsor


@receiver(pre_save, sender=Student)
def normalize_student_names(sender, instance, **kwargs):
    for field in ("first_name", "middle_name", "last_name"):
        value = getattr(instance, field, "")
        if value:
            setattr(instance, field, value.strip().title())


@receiver(post_save, sender=StudentSponsor)
def ensure_single_primary_sponsor(sender, instance, **kwargs):
    if instance.is_primary:
        (
            StudentSponsor.objects.filter(student=instance.student, is_primary=True)
            .exclude(pk=instance.pk)
            .update(is_primary=False)
        )

