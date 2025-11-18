from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Document, Enrollment


@receiver(pre_save, sender=Enrollment)
def enrollment_pre_save(sender, instance, **kwargs):
    if not instance.mutual_affiliate:
        instance.mutual_details = ""


@receiver(pre_save, sender=Document)
def document_pre_save(sender, instance, **kwargs):
    if instance.document_name:
        instance.document_name = instance.document_name.strip().title()

