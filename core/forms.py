from django import forms

from core.models import AcademicYear, Department, Faculty, Semester, Promotion


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: 2024-2025",
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: 24/25",
                "maxlength": "5",
            }),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Semestre 1",
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: S1",
                "maxlength": "5",
            }),
        }


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Sciences Économiques",
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: SE",
                "maxlength": "5",
            }),
        }


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Gestion",
            }),
            "code": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: GEST",
                "maxlength": "5",
            }),
            "faculty": forms.Select(attrs={
                "class": "form-control",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["faculty"].queryset = Faculty.objects.order_by("name")


class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ex: Promotion 2024",
            }),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["department"].queryset = Department.objects.order_by("name")

