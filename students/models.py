from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

class Address(models.Model):
    street = models.CharField(max_length=100)
    quarter = models.CharField(max_length=50)
    city_commune = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.street}, {self.quarter}"


class Contact(models.Model):
    phone_number = models.CharField(max_length=20)
    whatsapp_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Diploma(models.Model):
    institution = models.CharField(max_length=100)
    obtaining_year = models.CharField(max_length=4)
    diploma_number = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.diploma_number}"


class Parent(models.Model):
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    origin_country = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    address = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Sponsor(models.Model):
    sponsor_type = models.CharField(max_length=50)
    organization = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=150)

    def __str__(self):
        return self.organization


class Student(models.Model):
    GENDER_CHOICES = [
        ("masculin", "Masculin"),
        ("feminin", "Féminin"),
    ]

    # Lien OneToOne vers le Custom User
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_profile"
    )

    matricule = models.CharField(max_length=20, unique=True, null=True, blank=True)
    photo = models.ImageField(upload_to="students/photos/", null=True, blank=True)

    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    marital_status = models.CharField(max_length=50)
    birth_place = models.CharField(max_length=50)
    birth_date = models.DateField()
    nationality = models.CharField(max_length=50, default="CONGOLAISE")

    address = models.OneToOneField(Address, on_delete=models.SET_NULL, null=True, blank=True)
    contact = models.OneToOneField(Contact, on_delete=models.SET_NULL, null=True, blank=True)
    diploma = models.OneToOneField(Diploma, on_delete=models.SET_NULL, null=True, blank=True)

    father = models.OneToOneField(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name="father")
    mother = models.OneToOneField(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name="mother")

    sponsors = models.ManyToManyField(Sponsor, through="StudentSponsor")

    def generate_matricule(self):
        """Génère le matricule au format 0001-26/27"""

        current_year = timezone.now().year
        # Si nous sommes en 2025 (début de l'année académique 2025-2026),
        # l'année académique est '25/26'.
        if timezone.now().month >= 8: # Par exemple, si l'année académique commence en août
            start_year = str(current_year)[2:]
            end_year = str(current_year + 1)[2:]
        else: # Si nous sommes en 2026 mais dans les premiers mois de l'année académique 2025-2026
            start_year = str(current_year - 1)[2:]
            end_year = str(current_year)[2:]

        academic_year = f"{start_year}/{end_year}"

        # Trouver le dernier matricule de l'année académique en cours
        last_student = Student.objects.filter(
            matricule__startswith="", # Filtre pour s'assurer que le matricule est non nul
            matricule__endswith=academic_year
        ).order_by('-matricule').first()

        sequence_number = 1
        if last_student and last_student.matricule:
            # Extrait le numéro de séquence (e.g., '0001')
            try:
                # Le matricule est 'XXXX-YY/ZZ', on prend la première partie
                last_sequence = int(last_student.matricule.split('-')[0])
                sequence_number = last_sequence + 1
            except ValueError:
                # En cas d'erreur de format, on recommence à 1
                sequence_number = 1

        # Formate le numéro de séquence sur 4 chiffres (e.g., 1 -> '0001')
        matricule_sequence = str(sequence_number).zfill(4)

        return f"{matricule_sequence}-{academic_year}"

    def save(self, *args, **kwargs):
        # 1. Génération du matricule à la création
        if not self.pk and not self.matricule:
            # Seulement si c'est une nouvelle instance et que le matricule n'est pas déjà défini
            self.matricule = self.generate_matricule()

        is_new_instance = self.pk is None

        super().save(*args, **kwargs)

        # 2. Création ou mise à jour de l'utilisateur
        if is_new_instance and not self.user and self.contact and self.contact.email:
            try:
                # Par défaut, le mot de passe peut être une valeur temporaire ou générée (e.g., 'changemoi123')
                # Vous devez gérer l'envoi du mot de passe initial à l'utilisateur
                # Ou forcer une réinitialisation après la première connexion.
                default_password = 'changeme_initial_password'

                UserModel = get_user_model()
                user = UserModel.objects.create_user(
                    email=self.contact.email,
                    password=default_password,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    role='STUDENT',
                    # Optionnel: on peut définir le username comme le matricule si souhaité
                    username=self.matricule 
                )
                self.user = user
                # Sauvegarder à nouveau pour lier l'utilisateur au profil Student
                # Utilisez update_fields pour éviter une boucle infinie dans save()
                Student.objects.filter(pk=self.pk).update(user=user) 

            except Exception as e:
                # Gérer les cas où l'utilisateur ne peut pas être créé (e.g., email déjà utilisé)
                print(f"Erreur lors de la création de l'utilisateur pour l'étudiant {self.matricule}: {e}")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.matricule})"


class StudentSponsor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    contribution_type = models.CharField(max_length=100, default="Frais Académiques")
    annual_commitment = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    is_primary = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ("student", "sponsor")
        verbose_name = "Parrainage étudiant"
        verbose_name_plural = "Parrainages étudiants"

    def __str__(self):
        return f"{self.sponsor} -> {self.student}"