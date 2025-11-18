from django import forms
from core.models import AcademicYear, Semester, Faculty, Department
from students.models import Address, Contact, Diploma, Parent, Student
from .models import Document, Enrollment, EnrollmentRequest, SecondaryChoice


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        ORDER_BY_MAPPING = {
            'student': ("last_name", "first_name"),
            'semester': ("id",),
            'faculty': ("name",),
            'department': ("name",),
        }

        for name, field in self.fields.items():
            if hasattr(field, "queryset"):
                if name in ORDER_BY_MAPPING:
                    field.queryset = field.queryset.order_by(*ORDER_BY_MAPPING[name])


class SecondaryChoiceForm(forms.ModelForm):
    class Meta:
        model = SecondaryChoice
        fields = "__all__"


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = "__all__"


# ====================================================================
# Formulaire multi-niveaux pour demande d'inscription
# ====================================================================

class CompleteEnrollmentForm(forms.Form):
    """Formulaire complet qui combine Student + Address + Contact + Diploma + Parents + Enrollment"""
    
    # ========== Section: Données de l'étudiant ==========
    photo = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        "class": "form-control",
        "accept": "image/*",
    }))
    
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Prénom",
    }))
    
    middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom du milieu",
    }))
    
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom",
    }))
    
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, widget=forms.Select(attrs={
        "class": "form-select",
    }))
    
    marital_status = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "État civil",
        "list": "marital_statuses",
    }))
    
    birth_place = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Lieu de naissance",
    }))
    
    birth_date = forms.DateField(widget=forms.DateInput(attrs={
        "type": "date",
        "class": "form-control",
    }))
    
    nationality = forms.CharField(max_length=50, initial="CONGOLAISE", widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nationalité",
    }))
    
    # ========== Section: Adresse ==========
    address_street = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Rue, avenue, boulevard...",
    }))
    
    address_quarter = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Quartier",
    }))
    
    address_city_commune = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Ville/Commune",
    }))
    
    # ========== Section: Contact ==========
    contact_phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "+243 XXX XXX XXX",
    }))
    
    contact_whatsapp_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "+243 XXX XXX XXX (optionnel)",
    }))
    
    contact_email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "email@exemple.com",
    }))
    
    # ========== Section: Diplôme ==========
    diploma_institution = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom de l'institution",
    }))
    
    diploma_obtaining_year = forms.CharField(max_length=4, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "AAAA",
        "maxlength": "4",
    }))
    
    diploma_number = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Numéro du diplôme",
    }))
    
    diploma_section = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Section/Spécialité",
    }))
    
    diploma_percentage = forms.DecimalField(max_digits=5, decimal_places=2, widget=forms.NumberInput(attrs={
        "class": "form-control",
        "step": "0.01",
        "min": "0",
        "max": "100",
    }))
    
    # ========== Section: Père ==========
    father_first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Prénom",
    }))
    
    father_middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom du milieu",
    }))
    
    father_last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom",
    }))
    
    father_origin_country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Pays d'origine",
    }))
    
    father_province = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Province",
    }))
    
    father_address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Adresse complète",
    }))
    
    father_phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "+243 XXX XXX XXX",
    }))
    
    father_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "email@exemple.com (optionnel)",
    }))
    
    # ========== Section: Mère ==========
    mother_first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Prénom",
    }))
    
    mother_middle_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom du milieu",
    }))
    
    mother_last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Nom",
    }))
    
    mother_origin_country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Pays d'origine",
    }))
    
    mother_province = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Province",
    }))
    
    mother_address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Adresse complète",
    }))
    
    mother_phone_number = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "+243 XXX XXX XXX",
    }))
    
    mother_email = forms.EmailField(required=False, widget=forms.EmailInput(attrs={
        "class": "form-control",
        "placeholder": "email@exemple.com (optionnel)",
    }))
    
    # ========== Section: Inscription ==========
    year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all().order_by('-name'),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Année académique"
    )
    
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all().order_by('name'),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Semestre"
    )
    
    faculty = forms.ModelChoiceField(
        queryset=Faculty.objects.all().order_by('name'),
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Faculté"
    )
    
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Département"
    )
    
    promotion = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        "class": "form-control",
        "placeholder": "Ex: L1 Gestion",
    }))
    
    admission_exam = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "form-check-input",
    }))
    
    how_known = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": "3",
        "placeholder": "Comment avez-vous connu notre université ?",
    }))
    
    why_chosen = forms.CharField(widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": "3",
        "placeholder": "Pourquoi avez-vous choisi cette formation ?",
    }))
    
    mutual_affiliate = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        "class": "form-check-input",
    }))
    
    mutual_details = forms.CharField(required=False, widget=forms.Textarea(attrs={
        "class": "form-control",
        "rows": "2",
        "placeholder": "Détails de l'affiliation mutuelle (si applicable)",
    }))
    
    commitments_accepted = forms.BooleanField(widget=forms.CheckboxInput(attrs={
        "class": "form-check-input",
    }))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les départements selon la faculté sélectionnée (si formulaire soumis)
        if 'faculty' in self.data:
            try:
                faculty_id = int(self.data.get('faculty'))
                self.fields['department'].queryset = Department.objects.filter(faculty_id=faculty_id).order_by('name')
            except (ValueError, TypeError):
                # Si la valeur est invalide, laissez le queryset vide (par défaut)
                pass
        
        # CORRECTION APPLIQUÉE ICI pour éviter l'AttributeError
        # Charger les départements si le formulaire est lié à une instance (si c'était un ModelForm)
        elif hasattr(self, 'instance') and self.instance and hasattr(self.instance, 'faculty'):
            self.fields['department'].queryset = Department.objects.filter(faculty=self.instance.faculty).order_by('name')
        else:
            # Pour l'affichage initial (GET), le queryset peut être vide
            if not self.fields['department'].queryset:
                 self.fields['department'].queryset = Department.objects.none()
    
    def save(self):
        """Crée tous les objets liés"""
        # Créer l'adresse
        address = Address.objects.create(
            street=self.cleaned_data['address_street'],
            quarter=self.cleaned_data['address_quarter'],
            city_commune=self.cleaned_data['address_city_commune'],
        )
        
        # Créer le contact
        contact = Contact.objects.create(
            phone_number=self.cleaned_data['contact_phone_number'],
            whatsapp_number=self.cleaned_data.get('contact_whatsapp_number'),
            email=self.cleaned_data['contact_email'],
        )
        
        # Créer le diplôme
        diploma = Diploma.objects.create(
            institution=self.cleaned_data['diploma_institution'],
            obtaining_year=self.cleaned_data['diploma_obtaining_year'],
            diploma_number=self.cleaned_data['diploma_number'],
            section=self.cleaned_data['diploma_section'],
            percentage=self.cleaned_data['diploma_percentage'],
        )
        
        # Créer le père
        father = Parent.objects.create(
            first_name=self.cleaned_data['father_first_name'],
            middle_name=self.cleaned_data['father_middle_name'],
            last_name=self.cleaned_data['father_last_name'],
            origin_country=self.cleaned_data['father_origin_country'],
            province=self.cleaned_data['father_province'],
            address=self.cleaned_data['father_address'],
            phone_number=self.cleaned_data['father_phone_number'],
            email=self.cleaned_data.get('father_email'),
        )
        
        # Créer la mère
        mother = Parent.objects.create(
            first_name=self.cleaned_data['mother_first_name'],
            middle_name=self.cleaned_data['mother_middle_name'],
            last_name=self.cleaned_data['mother_last_name'],
            origin_country=self.cleaned_data['mother_origin_country'],
            province=self.cleaned_data['mother_province'],
            address=self.cleaned_data['mother_address'],
            phone_number=self.cleaned_data['mother_phone_number'],
            email=self.cleaned_data.get('mother_email'),
        )
        
        # Créer l'étudiant
        student = Student.objects.create(
            photo=self.cleaned_data.get('photo'),
            first_name=self.cleaned_data['first_name'],
            middle_name=self.cleaned_data['middle_name'],
            last_name=self.cleaned_data['last_name'],
            gender=self.cleaned_data['gender'],
            marital_status=self.cleaned_data['marital_status'],
            birth_place=self.cleaned_data['birth_place'],
            birth_date=self.cleaned_data['birth_date'],
            nationality=self.cleaned_data['nationality'],
            address=address,
            contact=contact,
            diploma=diploma,
            father=father,
            mother=mother,
        )
        
        # Créer l'inscription
        enrollment = Enrollment.objects.create(
            student=student,
            year=self.cleaned_data['year'],
            semester=self.cleaned_data['semester'],
            faculty=self.cleaned_data['faculty'],
            department=self.cleaned_data.get('department'),
            promotion=self.cleaned_data['promotion'],
            admission_exam=self.cleaned_data.get('admission_exam', False),
            how_known=self.cleaned_data['how_known'],
            why_chosen=self.cleaned_data['why_chosen'],
            mutual_affiliate=self.cleaned_data.get('mutual_affiliate', False),
            mutual_details=self.cleaned_data.get('mutual_details', ''),
            commitments_accepted=self.cleaned_data['commitments_accepted'],
        )
        
        return enrollment


class EnrollmentRequestForm(forms.ModelForm):
    """Formulaire pour créer une demande d'inscription (publique)"""
    
    class Meta:
        model = EnrollmentRequest
        fields = ['student_data', 'enrollment_data']
        widgets = {
            'student_data': forms.HiddenInput(),
            'enrollment_data': forms.HiddenInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Les champs sont cachés, les données seront sérialisées depuis CompleteEnrollmentForm