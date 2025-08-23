
import random
from datetime import date, timedelta

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils import timezone
from phonenumber_field.widgets import PhoneNumberPrefixWidget

from .models import *


# for authentication
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError(
                ("This account is inactive."),
                code='inactive',
            )

class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name']
        

class PatientForm(forms.ModelForm):
    
    class Meta:
        model=Patient
        fields=['gender','dob','mobile','address_line_1','postcode','city','state','country']
        widgets = {
            'mobile' : PhoneNumberPrefixWidget()
        }

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['profile_picture', 'mobile']
    
    
# To add doctor
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name']
        widgets = {
            'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['gender','dob','mobile','department','register_id','address_line_1','postcode','city','state','country','status']
        widgets = {
            'mobile' : PhoneNumberPrefixWidget()
        }

class AppointmentDateForm(forms.Form):
    appointment_date = forms.DateTimeField(
        label='Appointment Date',
        widget = forms.DateInput(attrs={
            'type': 'date', 
            'min': timezone.now().strftime('%Y-%m-%d'), 
            'max': (timezone.now() + timedelta(days=7)).strftime('%Y-%m-%d')}),
        input_formats=['%Y-%m-%d']
    )

    # def clean_appointment_date(self):
    #     appointment_date = self.cleaned_data['appointment_date']
    #     today = timezone.now()
    #     seven_days_later = today + timedelta(days=7)

    #     # Check if the appointment date is within the next 7 days
    #     if not (today <= appointment_date <= seven_days_later):
    #         raise forms.ValidationError("The appointment date must be within the next 7 days.")

    #     # Check if the appointment date is a Sunday
    #     if appointment_date.weekday() == 6:
    #         raise forms.ValidationError("Appointments cannot be booked on Sundays.")

    #     return appointment_date
class BookAppointment(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['AppointmentDate','TimeSlot','patient' , 'doctor']
        widgets = {
            'PatientPhoneNumber' : PhoneNumberPrefixWidget(),
        }
