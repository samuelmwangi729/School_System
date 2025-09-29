from django.db import models
from Users.models import User
from Subjects.models import Subject
from InstitutionClasses.models import InstitutionClass as Classes
from InstitutionClasses.models import ClassStatus

class Teacher(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teaching_roles")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="subject_teachers")
    form = models.ForeignKey(Classes, on_delete=models.CASCADE, related_name="class_teachers")
    status = models.CharField(max_length=20, choices=ClassStatus.choices, default=ClassStatus.ACTIVE)

    def __str__(self):
        return self.teacher.username
