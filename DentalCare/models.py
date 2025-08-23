
import django.utils.timezone
from django.contrib.auth.models import AbstractUser, Group, Permission, User
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


# USER
class User(AbstractUser):

    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

# Choices 
SYMPTOM_CHOICES = [
    ('TOOTHACHE', 'Toothache'),
    ('BLEEDING_GUMS', 'Bleeding Gums'),
    ('CAVITIES', 'Cavities'),
    ('SENSITIVE_TEETH', 'Sensitive Teeth'),
    ('BAD_BREATH', 'Bad Breath'),
    ('SWOLLEN_GUMS', 'Swollen Gums'),
    ('MOUTH_SORES', 'Mouth Sores'),
    ('JAW_PAIN', 'Jaw Pain'),
    ('BROKEN_TOOTH', 'Broken Tooth'),
    ('OTHER', 'Other'),
]

DEPARTMENT_CHOICES = [
    ('GENERAL_DENTISTRY', 'General Dentistry'),
    ('ORTHODONTICS', 'Orthodontics'),
    ('PEDIATRIC_DENTISTRY', 'Pediatric Dentistry'),
    ('PERIODONTICS', 'Periodontics'),
    ('ENDODONTICS', 'Endodontics'),
    ('PROSTHODONTICS', 'Prosthodontics'),
    ('ORAL_SURGERY', 'Oral Surgery'),
    ('COSMETIC_DENTISTRY', 'Cosmetic Dentistry'),
]

GENDER_CHOICES = [
    ('MALE','Male'),('FEMALE','Female'),('OTHERS','Others'),
]

COUNTRY_CHOICES = [
    ('UNITED STATES OF AMERICA','United States of America'),('INDIA','India'),('UNITED KINGDOM','United Kingdom'),
]

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/PatientProfilePic/', null=True, blank=True)
    gender= models.CharField(max_length=50,choices=GENDER_CHOICES, default='Male')
    dob = models.DateField()
    mobile = PhoneNumberField()
    address_line_1 = models.CharField(max_length=255)
    postcode = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='India')
    status=models.BooleanField(default=False)


    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Doctor(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    gender= models.CharField(max_length=50,choices=GENDER_CHOICES, default='Male')
    dob = models.DateField()
    mobile = PhoneNumberField()
    department= models.CharField(max_length=50,choices=DEPARTMENT_CHOICES,default='GENERAL_DENTISTRY')
    register_id = models.CharField(max_length=50)
    address_line_1 = models.CharField(max_length=255)
    postcode = models.IntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50, choices=COUNTRY_CHOICES, default='India')
    status=models.BooleanField(default=False)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        print(self.user.id)
        return self.user.id



class Appointment(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor=models.ForeignKey(Doctor, on_delete=models.CASCADE)
    symptoms = models.CharField(max_length=20, choices=SYMPTOM_CHOICES ,default='OTHER')
    AppointmentDate = models.DateField(default=django.utils.timezone.now)
    status=models.BooleanField(default=False)
    TimeSlot = models.TimeField(default=django.utils.timezone.now)
    AppointmentsDone = models.BooleanField(default=False)
    is_canceled = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Appointment on {self.AppointmentDate}",f"{self.patient.get_name}"


    def __str__(self) -> str:
        return f"{self.TimeSlot.strftime('%I:%M:%S')} , {self.AppointmentDate.strftime("%Y-%m-%d")}"
