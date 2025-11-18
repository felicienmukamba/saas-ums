from django.db import models
from django.utils import timezone
from core.models import AcademicYear, Semester, Faculty, Department
from students.models import Student


class EnrollmentRequest(models.Model):
    """Demande d'inscription soumise par un étudiant (publique, sans login)"""
    
    STATUS_CHOICES = [
        ('PENDING', 'En attente'),
        ('APPROVED', 'Approuvée'),
        ('REJECTED', 'Rejetée'),
    ]
    
    # Données de l'étudiant (sérialisées en JSON ou champs séparés)
    # On stocke les données brutes de la demande
    student_data = models.JSONField(default=dict, help_text="Données complètes de l'étudiant")
    enrollment_data = models.JSONField(default=dict, help_text="Données d'inscription")
    
    # Métadonnées
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    submitted_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_enrollment_requests'
    )
    review_notes = models.TextField(blank=True, help_text="Notes du chargé d'inscription")
    
    # Lien vers l'inscription créée si approuvée
    enrollment = models.OneToOneField(
        'Enrollment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enrollment_request'
    )
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "Demande d'inscription"
        verbose_name_plural = "Demandes d'inscription"
    
    def __str__(self):
        student_name = self.student_data.get('first_name', '') + ' ' + self.student_data.get('last_name', '')
        return f"Demande de {student_name} - {self.get_status_display()}"
    
    def approve(self, reviewer, notes=''):
        """Approuve la demande et crée l'inscription"""
        from students.models import Address, Contact, Diploma, Parent, Student as StudentModel
        from datetime import datetime
        
        # Créer l'adresse
        address_data = self.student_data.get('address', {})
        address = Address.objects.create(**address_data) if address_data else None
        
        # Créer le contact
        contact_data = self.student_data.get('contact', {})
        contact = Contact.objects.create(**contact_data) if contact_data else None
        
        # Créer le diplôme
        diploma_data = self.student_data.get('diploma', {})
        if diploma_data and 'percentage' in diploma_data:
            diploma_data['percentage'] = float(diploma_data['percentage'])
        diploma = Diploma.objects.create(**diploma_data) if diploma_data else None
        
        # Créer le père
        father_data = self.student_data.get('father', {})
        father = Parent.objects.create(**father_data) if father_data else None
        
        # Créer la mère
        mother_data = self.student_data.get('mother', {})
        mother = Parent.objects.create(**mother_data) if mother_data else None
        
        # Créer l'étudiant
        student_data = {k: v for k, v in self.student_data.items() 
                       if k not in ['address', 'contact', 'diploma', 'father', 'mother', 'photo']}
        # Convertir birth_date si c'est une chaîne
        if 'birth_date' in student_data and isinstance(student_data['birth_date'], str):
            student_data['birth_date'] = datetime.fromisoformat(student_data['birth_date']).date()
        
        student = StudentModel.objects.create(
            address=address,
            contact=contact,
            diploma=diploma,
            father=father,
            mother=mother,
            **student_data
        )
        
        # Créer l'inscription
        from core.models import AcademicYear, Semester, Faculty, Department
        enrollment = Enrollment.objects.create(
            student=student,
            year_id=self.enrollment_data.get('year'),
            semester_id=self.enrollment_data.get('semester'),
            faculty_id=self.enrollment_data.get('faculty'),
            department_id=self.enrollment_data.get('department'),
            promotion=self.enrollment_data.get('promotion', ''),
            admission_exam=self.enrollment_data.get('admission_exam', False),
            how_known=self.enrollment_data.get('how_known', ''),
            why_chosen=self.enrollment_data.get('why_chosen', ''),
            mutual_affiliate=self.enrollment_data.get('mutual_affiliate', False),
            mutual_details=self.enrollment_data.get('mutual_details', ''),
            commitments_accepted=self.enrollment_data.get('commitments_accepted', False),
        )
        
        # Mettre à jour la demande
        self.status = 'APPROVED'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.review_notes = notes
        self.enrollment = enrollment
        self.save()
        
        return enrollment
    
    def reject(self, reviewer, notes=''):
        """Rejette la demande"""
        self.status = 'REJECTED'
        self.reviewed_at = timezone.now()
        self.reviewed_by = reviewer
        self.review_notes = notes
        self.save()


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    promotion = models.CharField(max_length=100)

    admission_exam = models.BooleanField(default=False)
    how_known = models.TextField()
    why_chosen = models.TextField()

    mutual_affiliate = models.BooleanField(default=False)
    mutual_details = models.TextField(null=True, blank=True)
    commitments_accepted = models.BooleanField()

    class Meta:
        unique_together = ("student", "year", "semester")

    def __str__(self):
        return f"Enrollment {self.student}"


class SecondaryChoice(models.Model):
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    promotion = models.CharField(max_length=100)

    def __str__(self):
        return f"Choice for {self.enrollment}"


class Document(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    document_name = models.CharField(max_length=100)
    is_required = models.BooleanField()
    file_path = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("enrollment", "document_name")


