from django.db import models
from core.models import AcademicYear, Semester, Department

class Course(models.Model):
    course_name = models.CharField(max_length=150, unique=True)
    course_code = models.CharField(max_length=10, unique=True)
    credits = models.IntegerField()

    cm_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    td_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tp_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.course_name


class CourseOffering(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    promotion_name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("course", "academic_year", "semester", "department", "promotion_name")
