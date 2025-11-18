from django.db import models

class AcademicYear(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name

    # on save, desactive les ancien et active le new save
    def save(self, *args, **kwargs):
        if self.status == 'active':
            AcademicYear.objects.filter(status='active').update(status='inactive')
        else:
            AcademicYear.objects.filter(status='inactive').update(status='active')
        super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Année Académique"
        verbose_name_plural = "Années Académiques"
    


class Semester(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"


class Faculty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Faculté"
        verbose_name_plural = "Facultés"


class Department(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=5)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("faculty", "name")
        verbose_name = "Département"
        verbose_name_plural = "Départements"

    def __str__(self):
        return f"{self.name} - {self.faculty}"


class Promotion(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=5, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
    
    def __str__(self):
        return f"{self.name} - {self.department}"
