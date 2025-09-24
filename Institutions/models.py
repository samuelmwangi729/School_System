from django.db import models

# Create your models here.
class InstitutionStatus:
    ACTIVE = "active"
    SUSPENDED = "suspended"
    DELETED = "deleted"

    choices = (
        (ACTIVE, "active"),
        (SUSPENDED, "suspended"),
        (DELETED, "deleted"),
    )
class InstitutionCategory:
    NATIONAL="national"
    EXTRACOUNTY="extra_county"
    COUNTY="county"

    choices=(
        (NATIONAL,"national"),
        (EXTRACOUNTY,"extra_county"),
        (COUNTY,"county")
    )

class InstitutionType:
    DAY="day"
    BOARDING="boarding"

    choices=(
        (DAY,"day"),
        (BOARDING,"boarding")
    )
class InstitutionStudentType:
    BOYS="boys"
    GIRLS="girls"
    MIXED="mixed"

    choices=(
        (BOYS,"boys"),
        (GIRLS,"girls"),
        (MIXED,"mixed")
    )
class InstitutionSNE:
    YES=True
    NO=False

    choices=(
        (YES,True),
        (NO,False)
    )
    
class Institution(models.Model):
    name = models.CharField(max_length=100)
    subcounty = models.CharField(max_length=100)
    county = models.CharField(max_length=100)
    category = models.CharField(max_length=20,choices=InstitutionCategory.choices)
    institutionType = models.CharField(max_length=10,choices=InstitutionType.choices)
    studentGender = models.CharField(max_length=10,choices=InstitutionStudentType.choices)
    is_sne =  models.BooleanField(choices=InstitutionSNE.choices,default=InstitutionSNE.NO)

    def __str__(self):
        return self.name
    