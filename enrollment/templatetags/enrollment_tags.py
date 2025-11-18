from django import template

from enrollment.models import Enrollment

register = template.Library()


@register.simple_tag
def total_enrollments():
    return Enrollment.objects.count()

