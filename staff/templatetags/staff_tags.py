from django import template

from staff.models import CourseAssignment

register = template.Library()


@register.simple_tag
def total_assignments():
    return CourseAssignment.objects.count()

