from django import template
from django.contrib.auth import get_user_model

register = template.Library()
User = get_user_model()


@register.simple_tag
def total_users():
    return User.objects.count()

