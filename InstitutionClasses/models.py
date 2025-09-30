from django.db import models
from Institutions.models import Institution
# Create your models here.
class ClassStatus:
    ACTIVE="active"
    SUSPENDED="suspended"
    DELETED="deleted"
    GRADUATED="graduated"

    choices = (
        (ACTIVE,"active"),
        (SUSPENDED,"suspended"),
        (DELETED,"deleted"),
        (GRADUATED,"graduated")
        )
class InstitutionClass(models.Model):
    class_code = models.CharField(max_length=10,blank=False) #this is unique to bthe organization
    class_name = models.CharField(max_length=20,blank=False)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="classes")
    institution_status = models.CharField(max_length=40,choices=ClassStatus.choices,default=ClassStatus.ACTIVE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.class_name