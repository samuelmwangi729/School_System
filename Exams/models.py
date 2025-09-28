from django.db import models
from Institutions.models import Institution
from Users.models import User
from datetime import datetime 
# Create your models here.
class EXAMTERMS:
    ONE="One"
    TWO="Two"
    THREE="Three"
    
    choices=(
        (ONE,"One"),
        (TWO,"Two"),
        (THREE,"Three")
        )
class ExaminationStatus:
    ACTIVE="active" #be done
    SUSPENDED="suspended" #suspended that cant be done 
    DELETED="deleted" #when the exam was deleted
    RELEASED="released" #after the analysis is done
    PAUSED="paused" #stop entry of the marks

    choices = (
        (ACTIVE,"active"),
        (SUSPENDED,"suspended"),
        (DELETED,"deleted"),
        (RELEASED,"released"),
        (PAUSED,"paused"),
        )
class Exam(models.Model):
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="examinations")
    exam_name = models.CharField(max_length=50,blank=False,unique=True)
    exam_term = models.CharField(
        max_length=10,
        choices=EXAMTERMS.choices,
        default=EXAMTERMS.ONE
    )
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="created_exams",blank=False)
    exam_year = models.IntegerField(default=datetime.now().year)
    created_at = models.DateField(auto_now_add=True,auto_now=False)
    updated_at = models.DateField(auto_now_add=False,auto_now=True)
    exam_status = models.CharField(max_length=15,choices=ExaminationStatus.choices,default=ExaminationStatus.ACTIVE)

    def __str__(self):
        return self.exam_name