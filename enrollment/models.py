from django.db import models
from core.models import AcademicYear, Semester, Faculty, Department
from students.models import Student

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
