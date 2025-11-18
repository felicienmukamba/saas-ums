from django import template
from django.db.models import Sum

from fees.models import AcademicFee

register = template.Library()


@register.simple_tag
def total_academic_fee_records():
    return AcademicFee.objects.count()


@register.simple_tag
def total_academic_fee_amount():
    return AcademicFee.objects.aggregate(total=Sum("amount"))["total"] or 0

