from django.db import models
from django.forms import CharField
from Institutions.models import Institution
from Users.models import User
# Create your models here.
class SubjectStatus:
    ACTIVE="active"
    SUSPENDED="suspended"
    DELETED="deleted"

    choices=(
        (ACTIVE,"active"),
        (SUSPENDED,"suspended"),
        (DELETED,"deleted")
        )
class Subject(models.Model):
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="subjects")
    subject_code = models.IntegerField(blank=False)
    subject_name = models.CharField(blank=False,max_length=20)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_subjects")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=False,auto_now=True)
    status = models.CharField(max_length=10,choices=SubjectStatus.choices,default=SubjectStatus.ACTIVE)

    def __str__(self):
        return self.subject_name