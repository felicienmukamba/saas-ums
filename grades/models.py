from django.db import models
from enrollment.models import Enrollment
from courses.models import CourseOffering
from assessments.models import AssessmentType
from users.models import User

class Grade(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    assessment_type = models.ForeignKey(AssessmentType, on_delete=models.CASCADE)

    score = models.DecimalField(max_digits=5, decimal_places=2)
    grading_date = models.DateField()
    recorded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ("enrollment", "course_offering", "assessment_type")
