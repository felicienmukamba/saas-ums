from django import template

from grades.models import Grade

register = template.Library()


@register.simple_tag
def total_grades():
    return Grade.objects.count()

