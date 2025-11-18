from django import template

from courses.models import Course, CourseOffering

register = template.Library()


@register.simple_tag
def total_courses():
    return Course.objects.count()


@register.simple_tag
def total_course_offerings():
    return CourseOffering.objects.count()

