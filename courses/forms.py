from django import forms

from .models import Course, CourseOffering


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"


class CourseOfferingForm(forms.ModelForm):
    class Meta:
        model = CourseOffering
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if hasattr(field, "queryset"):
                field.queryset = field.queryset.order_by("name")

