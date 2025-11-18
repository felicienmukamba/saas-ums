from django import template

from assessments.models import AssessmentType

register = template.Library()


@register.simple_tag
def total_assessment_types():
    return AssessmentType.objects.count()

