from django import forms

from .models import AcademicFee, FeeCategory


class FeeCategoryForm(forms.ModelForm):
    class Meta:
        model = FeeCategory
        fields = "__all__"


class AcademicFeeForm(forms.ModelForm):
    class Meta:
        model = AcademicFee
        fields = "__all__"

