from django import template
from django.db.models import Sum

from expenses.models import Expense

register = template.Library()


@register.simple_tag
def total_expenses_amount():
    return Expense.objects.aggregate(total=Sum("amount"))["total"] or 0

