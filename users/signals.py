from django.db.models.signals import pre_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(pre_save, sender=User)
def user_pre_save(sender, instance, **kwargs):
    if not instance.username:
        instance.username = instance.email.split("@")[0]
    instance.username = instance.username.lower()

