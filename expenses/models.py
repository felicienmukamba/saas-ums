from django.db import models
from core.models import AcademicYear
from users.models import User   # si user interne

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Expense(models.Model):
    category = models.ForeignKey(ExpenseCategory, on_delete=models.CASCADE)
    year = models.ForeignKey(AcademicYear, on_delete=models.SET_NULL, null=True)

    expense_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    reference_number = models.CharField(max_length=100, unique=True)
    beneficiary = models.ForeignKey(User, on_delete=models.CASCADE)

    payment_status = models.CharField(max_length=50, default="Payé")

    def __str__(self):
        return f"{self.category} - {self.amount}"
