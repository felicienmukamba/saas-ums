from django.db import models
from courses.models import CourseOffering

class AssessmentType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    is_major = models.BooleanField()

    def __str__(self):
        return self.name


class AssessmentWeighting(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)
    weight_percentage = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        unique_together = ("course_offering", "assessment_type")
