import time
from datetime import date

from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Employee(models.Model):
    HospitalName = models.CharField(max_length=50)
    OwnerName = models.CharField(max_length=20)
    Email = models.EmailField()
    number = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    MobNo = models.CharField(validators=[number], max_length=10, blank=True)
    Password = models.CharField(max_length=110)
    ConfPasswd = models.CharField(max_length=110)
    Redirect_id_employee = models.CharField(max_length=20)
    hospitallogo = models.ImageField(upload_to='media/hospimg/',default='', blank=True, null=True)

    def __str__(self):
        return self.HospitalName


class Doc(models.Model):
    OpUserName = models.CharField(max_length=20)
    PasswordOp = models.CharField(max_length=110)
    ConfPasswdOp = models.CharField(max_length=110)

    OpImage = models.ImageField(upload_to='media/opimg/',default='', blank=True, null=True)

    LabUserName = models.CharField(max_length=20)
    PasswordLab = models.CharField(max_length=110)
    ConfPasswdLab = models.CharField(max_length=110)
    
    LabImage = models.ImageField(upload_to='media/labimg/',default='', blank=True, null=True)

    DocUserName = models.CharField(max_length=20)
    PasswordDoc = models.CharField(max_length=110)
    ConfPasswdDoc = models.CharField(max_length=110)
    DocImage = models.ImageField(upload_to='media/docimg/',default='', blank=True, null=True)
    number = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    DocNumber = models.CharField(
        validators=[number], max_length=10, blank=True)
    Redirect_id_doc = models.CharField(max_length=20)

    def __str__(self):
        return self.OpUserName


class Patient(models.Model):

    # gender,blood type,date of birth

    Name = models.CharField(max_length=30)
    Age = models.CharField(max_length=3)
    Place = models.CharField(max_length=40)
    DateOfBirth = models.CharField(max_length=40)
    BloodGroup = models.CharField(max_length=3)

    number2 = RegexValidator(regex=r'^\+?1?\d{9,15}$')
    PhoneNumber = models.CharField(
        validators=[number2], max_length=10, blank=True)

    PatientImage = models.ImageField(
        upload_to='media/patientimg/', default='', blank=True, null=True)

    XrayImage = models.ImageField(upload_to='media/xrayimg/',default='', blank=True, null=True)
    ScanType = models.CharField(max_length=30)

    GeneratedResult = models.CharField(max_length=30)
    DoctorDescription = models.TextField(max_length=50)

    DocResult = models.CharField(max_length=30)
    DocNumber = models.CharField(max_length=40)
    DocName = models.CharField(max_length=20)
    OpName = models.CharField(max_length=20)
    LabName = models.CharField(max_length=20)
    HospitalName = models.CharField(max_length=40)
    HospitalEmail = models.CharField(max_length=20)
    HospitalNumber = models.CharField(max_length=11)
    Redirect_id = models.CharField(max_length=20)
    HospitalName = models.CharField(max_length=25)
    Date = models.CharField(max_length=20)
    Time = models.CharField(max_length=20)

    def __str__(self):
        return self.Name


class Brain(models.Model):
    file = models.FileField(upload_to='media/temp/')


class News(models.Model):
    t = time.localtime()
    Time = time.strftime("%H:%M:%S", t)

    today = date.today()
    Date = today.strftime("%b-%d-%Y")

    Image = models.ImageField(upload_to='media/news/')
    News_name = models.CharField(max_length=50)
    Content = models.TextField()

class Comments(models.Model):
    Name = models.CharField(max_length=30)
    Email = models.EmailField()
    Message = models.CharField(max_length=100)

class Drugs(models.Model):
    GenericName = models.CharField(max_length=50)
    BrandName = models.CharField(max_length=100)
    ReviewedRxList = models.DateField()
    Link = models.CharField(max_length=100) 
    


