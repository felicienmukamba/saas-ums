from django.db import models
from enrollment.models import Enrollment
from fees.models import AcademicFee

class Payment(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    academic_fee = models.ForeignKey(AcademicFee, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    receipt_number = models.CharField(max_length=100, unique=True)

    class Meta:
        unique_together = ("enrollment", "academic_fee", "receipt_number")
