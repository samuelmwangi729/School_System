from django.db import models
from django.contrib.auth.models import  AbstractUser
from django.utils import timezone
from django.contrib.auth.models import UserManager
from django.utils.translation import gettext_lazy as _
from Institutions.models import Institution
import jwt
from datetime import datetime,timedelta
from django.conf import settings
from InstitutionClasses.models import InstitutionClass as Classes
# Create your models here.
class Roles:
    STUDENT = "student"
    TEACHER = "teacher"
    PRINCIPAL = "principal"
    DEPPRINCIPAL = "deputy_principal"
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"

    choices = (
        (STUDENT, 'student'),
        (TEACHER, 'teacher'),
        (PRINCIPAL, 'principal'),
        (DEPPRINCIPAL, 'deputy_principal'),
        (ADMIN, 'admin'),
        (SUPER_ADMIN, 'super_admin'),
    )
class Status:
    ACTIVE = "active"
    DELETED = "deleted"
    SUSPENDED = "suspended"
    EXPIRED = "expired"
    USED = "used"
    

    choices = (
        (ACTIVE, 'active'),
        (DELETED, 'deleted'),
        (SUSPENDED, 'suspended'),
        (EXPIRED, 'expired'),
        (USED, 'used'),
    )
#custom user manager 
class CustomUserManager(UserManager):
    '''
    This custom class defines how the users
    and the super users are created
    They also help enforce the emails are required
    '''
    def create_user(self,username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **extra_fields)
    #create the super user 
    def create_superuser(self,username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role",Roles.SUPER_ADMIN)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, email, password, **extra_fields)
    pass
#extend the default user
class User(AbstractUser):
    first_name = models.CharField(_("first name"), max_length=150, blank=False)
    last_name = models.CharField(_("last name"), max_length=150, blank=False)
    email = models.EmailField(_("email address"), blank=False,unique=True)
    adm_no = models.IntegerField(_("admission_number"),default=0)
    institution = models.ForeignKey(Institution,on_delete=models.CASCADE,related_name="users",blank=True,null=True)
    role = models.CharField(max_length=50,choices=Roles.choices,default=Roles.TEACHER)
    objects = CustomUserManager()
    user_class = models.ForeignKey(Classes,on_delete=models.CASCADE,null=True,blank=True,related_name="user_class")
    account_status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)


    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username","first_name","last_name","password"]


    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    #allow the app get the token 
    @property
    def token(self):
        token = jwt.encode({
            "username":self.username,
            "email":self.email,
            "exp":datetime.utcnow()+timedelta(hours=2)
            },
            settings.SECRET_KEY,algorithm='HS256'
            )
        return token

#track logins any time 
class LoginTracker(models.Model):
    username  = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="logins")
    hostname = models.CharField(max_length=1000)
    ip_address = models.CharField(max_length=100)
    login_time = models.DateField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.username
#track logouts

class LogoutTracker(models.Model):
    username = models.ForeignKey(User,on_delete=models.DO_NOTHING,related_name="logouts")
    logout_time = models.DateField(auto_now=False,auto_now_add=True)

    def __str__(self):
        return self.username

#password resets

class ResetTokens(models.Model):
    username = models.ForeignKey(User,models.DO_NOTHING,related_name="user")
    token = models.CharField(max_length=1000)
    reset_time = models.DateField(auto_now_add=True)
    token_status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)

    def __str__(self):
        return self.username