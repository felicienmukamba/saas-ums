from django import forms

from .models import (
    Address,
    Contact,
    Diploma,
    Parent,
    Sponsor,
    Student,
    StudentSponsor,
)


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = "__all__"


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"


class DiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        fields = "__all__"


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = "__all__"


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ("user", "sponsors")
        widgets = {
            "birth_date": forms.DateInput(attrs={"type": "date"}),
        }


class StudentSponsorForm(forms.ModelForm):
    class Meta:
        model = StudentSponsor
        fields = "__all__"

