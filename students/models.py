from django.db import models

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

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class StudentSponsor(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("student", "sponsor")
