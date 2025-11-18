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
        widgets = {
            "street": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Rue, avenue, boulevard...",
            }),
            "quarter": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Quartier",
            }),
            "city_commune": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Ville/Commune",
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
        widgets = {
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+243 XXX XXX XXX",
            }),
            "whatsapp_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+243 XXX XXX XXX (optionnel)",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "email@exemple.com",
            }),
        }


class DiplomaForm(forms.ModelForm):
    class Meta:
        model = Diploma
        fields = "__all__"
        widgets = {
            "institution": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de l'institution",
            }),
            "obtaining_year": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "AAAA",
                "maxlength": "4",
            }),
            "diploma_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Numéro du diplôme",
            }),
            "section": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Section/Spécialité",
            }),
            "percentage": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
                "max": "100",
            }),
        }


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = "__all__"
        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Prénom",
            }),
            "middle_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du milieu",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom",
            }),
            "origin_country": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Pays d'origine",
            }),
            "province": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Province",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Adresse complète",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+243 XXX XXX XXX",
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "email@exemple.com (optionnel)",
            }),
        }


class SponsorForm(forms.ModelForm):
    class Meta:
        model = Sponsor
        fields = "__all__"
        widgets = {
            "sponsor_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Type de sponsor",
                "list": "sponsor_types",
            }),
            "organization": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom de l'organisation",
            }),
            "phone_number": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "+243 XXX XXX XXX",
            }),
            "address": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Adresse complète",
            }),
        }


class StudentForm(forms.ModelForm):
    # Champs avec datalist pour les relations
    address_street = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Rue",
            "list": "address_streets",
        }),
        label="Rue (adresse)"
    )
    
    contact_email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "email@exemple.com",
            "list": "contact_emails",
        }),
        label="Email (contact)"
    )

    class Meta:
        model = Student
        exclude = ("user", "sponsors", "matricule")
        widgets = {
            "photo": forms.FileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Prénom",
            }),
            "middle_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom du milieu",
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nom",
            }),
            "gender": forms.Select(attrs={
                "class": "form-select",
            }),
            "marital_status": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "État civil",
                "list": "marital_statuses",
            }),
            "birth_place": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Lieu de naissance",
            }),
            "birth_date": forms.DateInput(attrs={
                "type": "date",
                "class": "form-control",
            }),
            "nationality": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nationalité",
                "value": "CONGOLAISE",
            }),
            "address": forms.Select(attrs={
                "class": "form-select",
            }),
            "contact": forms.Select(attrs={
                "class": "form-select",
            }),
            "diploma": forms.Select(attrs={
                "class": "form-select",
            }),
            "father": forms.Select(attrs={
                "class": "form-select",
            }),
            "mother": forms.Select(attrs={
                "class": "form-select",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Améliorer les querysets pour les ForeignKeys
        if self.fields.get("address"):
            self.fields["address"].queryset = Address.objects.all().order_by("street")
        if self.fields.get("contact"):
            self.fields["contact"].queryset = Contact.objects.all().order_by("email")
        if self.fields.get("diploma"):
            self.fields["diploma"].queryset = Diploma.objects.all().order_by("institution")
        if self.fields.get("father"):
            self.fields["father"].queryset = Parent.objects.all().order_by("last_name", "first_name")
        if self.fields.get("mother"):
            self.fields["mother"].queryset = Parent.objects.all().order_by("last_name", "first_name")


class StudentSponsorForm(forms.ModelForm):
    class Meta:
        model = StudentSponsor
        fields = "__all__"
        widgets = {
            "student": forms.Select(attrs={
                "class": "form-select",
            }),
            "sponsor": forms.Select(attrs={
                "class": "form-select",
            }),
            "contribution_type": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Type de contribution",
            }),
            "annual_commitment": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01",
                "min": "0",
            }),
            "is_primary": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": "3",
                "placeholder": "Notes additionnelles...",
            }),
        }
