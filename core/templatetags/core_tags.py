from django import template

from core.models import AcademicYear, Department, Faculty, Semester

register = template.Library()


@register.simple_tag
def total_academic_years():
    return AcademicYear.objects.count()


@register.simple_tag
def total_semesters():
    return Semester.objects.count()


@register.simple_tag
def total_faculties():
    return Faculty.objects.count()


@register.simple_tag
def total_departments():
    return Department.objects.count()

