from django import forms

from .models import Document, Enrollment, SecondaryChoice


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if hasattr(field, "queryset"):
                field.queryset = field.queryset.order_by("name")


class SecondaryChoiceForm(forms.ModelForm):
    class Meta:
        model = SecondaryChoice
        fields = "__all__"


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"

