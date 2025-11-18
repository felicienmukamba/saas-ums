from django import template
from django.db.models import Sum
from django.utils import timezone

from payments.models import Payment

register = template.Library()


@register.simple_tag
def payments_current_year():
    now = timezone.now()
    start = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
    total = Payment.objects.filter(payment_date__gte=start).aggregate(total=Sum("amount_paid"))["total"]
    return total or 0


@register.simple_tag
def total_payments():
    return Payment.objects.count()

