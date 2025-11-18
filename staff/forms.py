from django import forms

from .models import CourseAssignment


class CourseAssignmentForm(forms.ModelForm):
    class Meta:
        model = CourseAssignment
        fields = "__all__"

