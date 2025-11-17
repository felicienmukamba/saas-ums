from django.db import models
from courses.models import CourseOffering
from users.models import User

class CourseAssignment(models.Model):
    course_offering = models.ForeignKey(CourseOffering, on_delete=models.CASCADE)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    assignment_role = models.CharField(max_length=50)

    class Meta:
        unique_together = ("course_offering", "teacher", "assignment_role")
