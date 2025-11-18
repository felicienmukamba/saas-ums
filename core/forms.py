from django import forms

from .models import AcademicYear, Department, Faculty, Semester


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        fields = "__all__"


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = "__all__"


class FacultyForm(forms.ModelForm):
    class Meta:
        model = Faculty
        fields = "__all__"


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["faculty"].queryset = Faculty.objects.order_by("name")

