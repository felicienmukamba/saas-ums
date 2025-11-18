from django import template

from students.models import Student

register = template.Library()


@register.simple_tag
def total_students():
    return Student.objects.count()

