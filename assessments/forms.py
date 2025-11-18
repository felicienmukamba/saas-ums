from django import forms

from .models import AssessmentType, AssessmentWeighting


class AssessmentTypeForm(forms.ModelForm):
    class Meta:
        model = AssessmentType
        fields = "__all__"


class AssessmentWeightingForm(forms.ModelForm):
    class Meta:
        model = AssessmentWeighting
        fields = "__all__"

