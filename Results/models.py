from django.db import models
from Institutions.models import Institution
from Exams.models import EXAMTERMS, Exam
from Users.models import User
from Subjects.models import Subject
from datetime import datetime
from InstitutionClasses.models import InstitutionClass as student_class
# Create your models here.
class Result(models.Model):
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="institution_results")
    exam = models.ForeignKey(Exam,on_delete=models.CASCADE,related_name="exam_results")
    term = models.CharField(max_length=5,choices=EXAMTERMS.choices,blank=False)
    year = models.DateField(default=datetime.now().year)
    form = models.ForeignKey(student_class,on_delete=models.CASCADE,related_name="student_class",null=True,blank=True)
    teacher = models.ForeignKey(User,on_delete=models.CASCADE,related_name="teacher_results")
    student = models.ForeignKey(User,on_delete=models.CASCADE,related_name="student_results")
    subject =models.ForeignKey(Subject,on_delete=models.CASCADE,related_name="subject_results")
    mark = models.IntegerField(default=-1)
    grade = models.CharField(max_length=8) #create a relationship with the grading table
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


    def _str__(self):
        return self.exam