from datetime import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import redirect, render

from DentalCare.forms import *
from DentalCare.utils import generate_profile_picture, send_sms

# Create your views here.
User = get_user_model()


# Main Landing Page
def index(request):
    return render(request, 'DentalCare/index.html')


# Dashboard Page for All Users
def home_page_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'DentalCare/index.html')

# For logout
def logout_view(request):
    logout(request)
    return render(request,'DentalCare/index.html')

# For Sign Up / Login
# ADMIN
def admin_view_afterlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'DentalCare/adminlogin.html')

# DOCTOR
def doctor_view_afterlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'DentalCare/doctorlogin.html')

# PATIENT
def patient_view_afterlogin(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'DentalCare/patientlogin.html')


# --------------------------------------------------------------------------------------

# For Checking Type of User

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    print("Patient")
    return user.groups.filter(name='PATIENT').exists()


# For dashbaord page after login of user
def afterlogin_view(request):
    
    # For ADMIN
    if is_admin(request.user):
        return redirect('admin-dashboard')
    
    # For DOCTOR
    elif is_doctor(request.user):
        accountapproval=Doctor.objects.filter(user_id=request.user.id,status=True).exists()
        if accountapproval:
            return redirect('doctor-dashboard')
        
    # For PATIENT
    elif is_patient(request.user):
        # print("User is patient")
        # accountapproval=Patient.objects.filter(user_id=request.user.id,status=True).exists()
        # print(accountapproval)
        # if accountapproval:
        return redirect('patient-dashboard')
        # else:
        #     return HttpResponse("NOT Patient") 
    else:
        return render(request , 'index.html')

# --------------------------------- PATIENT --------------------------------------------

import logging
import random

from django.contrib.auth.hashers import check_password

logger = logging.getLogger(__name__)

# For Patient Sign Up
def patient_signup_view(request):
    userForm=PatientUserForm()
    patientForm=PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user = userForm.save(commit=False)

            username = userForm.cleaned_data['first_name'].lower() + str(random.randint(1000, 9999))
            user.username = username
            password = username
            user.set_password(password)
            
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user

            profile_picture = generate_profile_picture(user)
            patient.profile_picture = profile_picture

            patient.save()
            
            phone_number = patientForm.cleaned_data['mobile']
            phone_number_str = phone_number.as_e164

            send_sms(phone_number_str, f"You have been registered to Oral Fix Dental Clinic. Your Username is {user.username} and Password is {password}.")

            my_patient_group = Group.objects.get(name='PATIENT')
            user.groups.add(my_patient_group)

            login(request, user)
            return redirect('home_page')
        else:
            logger.error(userForm.errors)
            logger.error(patientForm.errors)
        
        return HttpResponseRedirect('patient-login')
    return render(request,'DentalCare/patientsignup.html',context=mydict)

# Login for patient
def custom_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home_page')
            
            else:
                # print(f"Failed to authenticate user: {username}")
                # print(f"Password correct: {check_password(password, User.objects.get(username=username).password)}")
                return render(request, 'DentalCare/patientlogin.html', {'form': form, 'error': 'Invalid username or password'})
        else:
            # print("Form is not valid")
            # print(form.errors)
            return render(request, 'DentalCare/patientlogin.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'DentalCare/patientlogin.html', {'form': form})

# For patient dashboard
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    print("patient-dashboard")
    patient = Patient.objects.get(user_id=request.user.id)

    # Fetch appointments
    upcoming_appointments = Appointment.objects.filter(patient=patient, is_canceled=False, AppointmentDate__gte=timezone.now())
    canceled_appointments = Appointment.objects.filter(patient=patient, is_canceled=True)
    past_appointments = Appointment.objects.filter(patient=patient, is_canceled=False, AppointmentDate__lt=timezone.now())

    # Count appointments
    upcoming_count = upcoming_appointments.count()
    canceled_count = canceled_appointments.count()
    past_count = past_appointments.count()

    mydict = {
        'patient': patient,
        'upcoming_count': upcoming_count,
        'canceled_count': canceled_count,
        'past_count': past_count,
    }
    
    # try:
    #     patient = Patient.objects.get(user_id=request.user.id)
    #     print(f"Patient found: {patient}")
    # except Patient.DoesNotExist:
    #     print("Patient does not exist for user_id:", request.user.id)
    #     return HttpResponseNotFound("Patient not found")
    # except Exception as e:
    #     print(f"Unexpected error: {e}")
    #     return HttpResponseNotFound("An unexpected error occurred")

    
    return render(request, 'DentalCare/patient_dashboard.html', context=mydict)
    


# To book appointments
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def book_appointment_date(request):
    date_form = AppointmentDateForm()
    # current_time = timezone.now()
    # end_date = current_time + timedelta(days=7)
    # # Date Slots
    # min_date = current_time.strftime('%Y-%m-%d')
    # max_date = end_date.strftime('%Y-%m-%d')
    
    if request.method == "POST":
        date_form = AppointmentDateForm(request.POST)
        if date_form.is_valid():
            appointment_date = date_form.cleaned_data['appointment_date']
            formatted_date = appointment_date.strftime('%Y-%m-%d')
            
            if formatted_date:
                return redirect('book-appointment' , appointment_date = formatted_date)

    return render(request,'DentalCare/appointment_date.html',{'date_form':date_form})

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def book_appointment(request,appointment_date):
    appointment_date = request.GET.get('appointment_date',appointment_date)
    appointment_date_formatted = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    specified_time_slots = [
        '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', 
        '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM',
        '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM',
        '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM'
    ]

    existing_appointments = Appointment.objects.filter(AppointmentDate=appointment_date_formatted).values_list('TimeSlot',flat = True)
    print(existing_appointments)

    formatted_time_slots = [time_obj.strftime('%I:%M %p') for time_obj in existing_appointments]
    print(formatted_time_slots)

    available_time_slots = [time_slot for time_slot in specified_time_slots if time_slot not in formatted_time_slots]
    print(available_time_slots)
    if request.method == "POST":
        appointment_form = BookAppointment(request.POST)

        print(appointment_form.errors)
        if appointment_form.is_valid():
            print(appointment_form.errors)

            # appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

        
            adjusted_appointment_time = appointment_time.replace(" AM", ":00").replace(" PM", ":00")

            user = request.user
            patient = Patient.objects.get(user = user)

            symptoms = appointment_form.cleaned_data['symptoms']
            department_name = assign_doctor(symptoms)
            doctor = Doctor.objects.filter(department=department_name).first()

            if not doctor:
                doctor = Doctor.objects.filter(department='General Dentistry').first()

            if doctor:
                patient_appointment = Appointment(
                    patient = patient,
                    doctor = doctor ,
                    AppointmentDate = appointment_date,
                    TimeSlot = adjusted_appointment_time, 
                    symptoms = symptoms)
                
                
                patient_appointment.save()

                phone_number_str = patient.mobile.as_e164

                send_sms(phone_number_str, f"Hello, {user.first_name}, You appointment with OralFix Dental Care has been scheduled for {appointment_date} and {appointment_time}. Your Attending Doctor is Dr. {doctor.get_name}.Please arrive 10 minutes before your scheduled appointment time.If you have any questions or need to reschedule, please contact the Doctor at {doctor.mobile}.")

                messages.success(request, "Appointment Booked Successfully!")
                return redirect('patient-view-appointment') 
            else:
                print(appointment_form.errors)
                return render(request, 'DentalCare/bookappointment.html', {'appointment_form': appointment_form, 'error': 'No doctor available' , 'appointment_date' : appointment_date })
            
    else:
        appointment_form = BookAppointment()

    return render(request, 'DentalCare/bookappointment.html', {'appointment_date': appointment_date , 'available_time_slots': available_time_slots , 'appointment_form' : appointment_form} )


# To assign doctor to patient according to symptoms
def assign_doctor(symptoms):
    symptom_to_department = {
        'TOOTHACHE': 'ENDODONTICS',
        'BLEEDING_GUMS': 'PERIODONTICS',
        'CAVITIES': 'GENERAL_DENTISTRY',
        'SENSITIVE_TEETH': 'GENERAL_DENTISTRY',
        'BAD_BREATH': 'GENERAL_DENTISTRY',
        'SWOLLEN_GUMS': 'PERIODONTICS',
        'MOUTH_SORES': 'ORAL SURGERY',
        'JAW_PAIN': 'ORAL SURGERY',
        'BROKEN_TOOTH': 'RESTRORATIVE DENTISTRY',
        'OTHER': 'GENERAL_DENTISTRY'
    }
    return symptom_to_department.get(symptoms.upper(), 'General Dentistry')


# View Appointments
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def patient_view_appointment(request):
    patient=Patient.objects.get(user_id=request.user.id)

    now = timezone.now()
    upcoming_appointments = Appointment.objects.filter(patient=patient, AppointmentDate__gte=now, is_canceled = False).order_by('AppointmentDate')
    past_appointments = Appointment.objects.filter(patient=patient, AppointmentDate__lt=now, is_canceled=False).order_by('-AppointmentDate')
    canceled_appointments = Appointment.objects.filter(patient = patient, is_canceled = True).order_by('AppointmentDate')
    mydict = {
        'patient': patient,
        'upcoming_appointments': upcoming_appointments,
        'past_appointments': past_appointments,
        'canceled_appointments':canceled_appointments,
    }
    return render(request,'DentalCare/view-appointments-patient.html',context=mydict)

# Cancellation of Appointment
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def cancel_appointment(request, appointment_id):

    appointment = Appointment.objects.get(id=appointment_id, patient__user=request.user)
    appointment.is_canceled = True
    appointment.save()

    patient = Patient.objects.get(user_id = request.user.id)
    phone_number_str = patient.mobile.as_e164
    send_sms(phone_number_str, 'Your Appointment has been successfully canceled.')
    
    return redirect('patient-view-appointment')

# Profile
@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def view_profile(request):
    patient = Patient.objects.get(user=request.user)
    return render(request, 'DentalCare/view_profile.html', {'patient': patient})

@login_required(login_url='patient-login')
@user_passes_test(is_patient)
def update_profile(request):
    patient = Patient.objects.get(user=request.user)

    if request.method == "POST":
        profileForm = PatientProfileForm(request.POST, request.FILES, instance=patient)
        userForm = PatientUserForm(request.POST,instance=request.user)
        if profileForm.is_valid() & userForm.is_valid():
            profileForm.save()
            userForm.save()
            return redirect('view_profile')
    else:
        form = PatientProfileForm(instance=patient)
    return render(request, 'DentalCare/update_profile.html', {'profileForm': profileForm, 'userForm' : userForm ,'patient': patient})


# -------------------------------- ADMIN -----------------------------------------------

# Admin Dashboard
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=Doctor.objects.all().order_by('-id')
    patients=Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=Doctor.objects.all().filter(status=False).count()

    patientcount=Patient.objects.all().count()
    pendingpatientcount=Patient.objects.all().filter(status=False).count()

    upcomingappointmentcount=Appointment.objects.all().filter(AppointmentDate__gte=timezone.now(),is_canceled = False).count()
    pastappointmentcount=Appointment.objects.all().filter(AppointmentDate__lte=timezone.now()).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'upcomingappointmentcount':upcomingappointmentcount,
    'pastappointmentcount':pastappointmentcount,
    'current_date':timezone.now
    }
    return render(request,'DentalCare/admin_dashboard.html',context=mydict)

# Doctor Views for Admin

# View Doctor
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def view_doctor(request):
    doctors=Doctor.objects.all().filter(status=True)
    return render(request,'DentalCare/view_all_doctor.html',{'doctors':doctors,'current_date':timezone.now})

# Add Doctor
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def add_doctor(request):
    userForm=DoctorUserForm()
    doctorForm=DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm,'current_date':timezone.now}
    if request.method=='POST':
        userForm=DoctorUserForm(request.POST)
        doctorForm=DoctorForm(request.POST)
        print(userForm.errors)
        print(doctorForm.errors)
        if userForm.is_valid() and doctorForm.is_valid():

            user=userForm.save(commit=False)
            username = userForm.cleaned_data['first_name'].lower() + str(random.randint(1000, 9999))

            user.username = username
            password = user.username
            user.set_password(password)
            user.is_doctor = True
            user.save()

            doctor=doctorForm.save(commit=False)

            profile_picture = generate_profile_picture(user)
            doctor.profile_picture = profile_picture

            doctor.user = user

            # Add the user to the 'Doctors' group
            doctor_group = Group.objects.get(name='DOCTOR')
            user.groups.add(doctor_group)

            doctor.status=True
            doctor.save()

            phone_number = doctorForm.cleaned_data['mobile']
            phone_number_str = phone_number.as_e164

            username = user.username

            send_sms(phone_number_str, f"You have been registered to OralFix Dental Care as a Doctor. Your Username is {username} and Passowrd is {password}")

        return HttpResponseRedirect('view-doctor')
    return render(request,'DentalCare/add_doctor.html',context=mydict)

# Doctor Profile
def doctor_profile_view(request, doctor_id):
    doctor = Doctor.objects.get(id=doctor_id)
    return render(request, 'DentalCare/doctor_profile.html', {'doctor': doctor})

# Update Doctor
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.user_id)

    userForm=DoctorUserForm(instance=user)
    doctorForm=DoctorForm(instance=doctor)

    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=DoctorUserForm(request.POST,instance=user)
        doctorForm=DoctorForm(request.POST,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            
            user=userForm.save()
            username = userForm.cleaned_data['first_name'].lower() + str(random.randint(1000, 9999))
            user.username = username
            password = username
            user.set_password(password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()

            phone_number = doctorForm.cleaned_data['mobile']
            phone_number_str = phone_number.as_e164

            send_sms(phone_number_str, f"Your Profile on OralFix Dental Care as a Doctor has been updated. Your Username is {username} and Passowrd is {password}")

            messages.success(request,'Doctor Profile Updated Successfully!')

            return redirect('view-doctor')
    return render(request,'DentalCare/update_doctor.html',context=mydict)


# Delete Doctors
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor(request,pk):
    doctor=Doctor.objects.get(id=pk)
    user=User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    messages.success(request,'Doctor Profile Deleted Successfully!')

    return redirect('view-doctor')


# For viewing patient in admin dashboard

# View Patient
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def view_patient(request):
    patients=Patient.objects.all()
    return render(request,'DentalCare/view_all_patient.html',{'patients':patients})

# Patient Profile
def patient_profile_view(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    return render(request, 'DentalCare/patient-profile.html', {'patient': patient})

# Update Patient
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)

    userForm=PatientUserForm(instance=user)
    patientForm=PatientForm(instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}

    if request.method=='POST':
        userForm=PatientUserForm(request.POST,instance=user)
        patientForm=PatientForm(request.POST,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient=patient.save()

            messages.success(request,'Patient Profile Updated Successfully!')

            return redirect('view-patient')
    return render(request,'DentalCare/update-patient.html',context=mydict)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_patient(request,pk):
    patient=Patient.objects.get(id=pk)
    user=User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()

    messages.success(request,'Patient Profile Deleted Successfully!')
    return redirect('view-patient')

# Add Patient
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def add_patient(request):
    userForm=PatientUserForm()
    patientForm=PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save(commit=False)
            
            username = userForm.cleaned_data['first_name'].lower() + str(random.randint(1000, 9999))
            user.username = username
            password = username
            
            user.set_password(password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user

            profile_picture = generate_profile_picture(user)
            patient.profile_picture = profile_picture

            patient.status=True
            patient.save()

            my_patient_group = Group.objects.get(name='PATIENT')
            user.groups.add(my_patient_group)

            phone_number = patientForm.cleaned_data['mobile']
            phone_number_str = phone_number.as_e164

            send_sms(phone_number_str, f"You have been registered to Oral Fix Dental Clinic. Your Username is {user.username} and Password is {password}.")

            messages.success(request,'Patient Profile Added Successfully!')



        return HttpResponseRedirect('view-patient')
    return render(request,'DentalCare/add-patient.html',context=mydict)

# Appointments

# View Appointments

# To book appointments
@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def book_appointment_date_admin(request):
    date_form = AppointmentDateForm()
    # current_time = timezone.now()
    # end_date = current_time + timedelta(days=7)
    # # Date Slots
    # min_date = current_time.strftime('%Y-%m-%d')
    # max_date = end_date.strftime('%Y-%m-%d')
    
    if request.method == "POST":
        date_form = AppointmentDateForm(request.POST)
        if date_form.is_valid():
            appointment_date = date_form.cleaned_data['appointment_date']
            formatted_date = appointment_date.strftime('%Y-%m-%d')
            
            if formatted_date:
                return redirect('book-appointment-admin' , appointment_date = formatted_date)

    return render(request,'DentalCare/appointment_date_admin.html',{'date_form':date_form})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def book_appointment_admin(request,appointment_date):
    appointment_date = request.GET.get('appointment_date',appointment_date)
    appointment_date_formatted = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    specified_time_slots = [
        '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', 
        '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM',
        '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM',
        '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM'
    ]

    existing_appointments = Appointment.objects.filter(AppointmentDate=appointment_date_formatted).values_list('TimeSlot',flat = True)
    print(existing_appointments)

    formatted_time_slots = [time_obj.strftime('%I:%M %p') for time_obj in existing_appointments]
    print(formatted_time_slots)

    available_time_slots = [time_slot for time_slot in specified_time_slots if time_slot not in formatted_time_slots]
    print(available_time_slots)

    patients = Patient.objects.all()
    patient_name = []
    for patient in patients:
        patient_name.append(f"{patient.user.first_name} {patient.user.last_name}") 
    print(patient_name)

    if request.method == "POST":
        appointment_form = BookAppointment(request.POST)

        print(appointment_form.errors)
        if appointment_form.is_valid():
            print(appointment_form.errors)

            # appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

        
            adjusted_appointment_time = appointment_time.replace(" AM", ":00").replace(" PM", ":00")

            
            patient = request.POST.get('patient')
            patient = patient.split()
            first_name , last_name = patient
            
            patient = Patient.objects.filter(user__first_name = first_name, user__last_name = last_name).first()
            print(patient)

            symptoms = appointment_form.cleaned_data['symptoms']
            # print(symptoms)
            department_name = assign_doctor(symptoms)
            # print(department_name)
            doctor = Doctor.objects.filter(department=department_name).first()
            # print(doctor)
            
            
            if doctor:
                # print("Y")
                patient_appointment = Appointment(
                    patient = patient,
                    doctor = doctor ,
                    AppointmentDate = appointment_date,
                    TimeSlot = adjusted_appointment_time, 
                    symptoms = symptoms)
                
                
                patient_appointment.save()

                phone_number_str = patient.mobile.as_e164

                send_sms(phone_number_str, f"Hello, {patient.user.first_name}, You appointment with OralFix Dental Care has been scheduled for {appointment_date} and {appointment_time}. Your Attending Doctor is Dr. {doctor.get_name}.Please arrive 10 minutes before your scheduled appointment time.If you have any questions or need to reschedule, please contact the Doctor at {doctor.mobile}.")

                messages.success(request, "Appointment Booked Successfully!")


                return redirect('view-appointment') 
            else:
                print(appointment_form.errors)
                return render(request, 'DentalCare/book-appointment-admin.html', {'appointment_form': appointment_form, 'error': 'No doctor available' , 'appointment_date' : appointment_date })
            
    else:
        appointment_form = BookAppointment()

    return render(request, 'DentalCare/book-appointment-admin.html', {'appointment_date': appointment_date , 'available_time_slots': available_time_slots , 'appointment_form' : appointment_form , 'patient_name' : patient_name} )

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def view_all_appointment(request):
    appointments=Appointment.objects.all()
    return render(request,'DentalCare/view_all_appointments.html',{'appointments':appointments})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def cancel_appointment_admin(request, appointment_id):

    appointment = Appointment.objects.get(id=appointment_id)
    appointment.is_canceled = True
    appointment.save()

    doctor = Doctor.objects.get(user_id = request.user.id)
    phone_number_str = doctor.mobile.as_e164

    patient = Patient.objects.get(user_id = appointment.patient.get_id())
    phone_number_str = patient.mobile.as_e164

    send_sms(phone_number_str, 'Your Appointment has been successfully canceled.')
    messages.success(request, "Appointment Cancelled Successfully!")

    return redirect('view-appointment-doctor')



@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    
    doctor = Doctor.objects.get(user_id=request.user.id)


    # Fetch appointments
    upcoming_appointments = Appointment.objects.filter(doctor=doctor, is_canceled=False, AppointmentDate__gte=timezone.now())
    canceled_appointments = Appointment.objects.filter(doctor=doctor, is_canceled=True)
    past_appointments = Appointment.objects.filter(doctor=doctor, is_canceled=False, AppointmentDate__lt=timezone.now())

    # Count appointments
    upcoming_count = upcoming_appointments.count()
    canceled_count = canceled_appointments.count()
    past_count = past_appointments.count()
    
    mydict={
        'current_date':timezone.now,
        'upcoming_count': upcoming_count,
        'canceled_count': canceled_count,
        'past_count': past_count,
    }
    return render(request,'DentalCare/doctor_dashboard.html',context=mydict)



# To book appointments
@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def book_appointment_date_doctor(request):
    date_form = AppointmentDateForm()
    # current_time = timezone.now()
    # end_date = current_time + timedelta(days=7)
    # # Date Slots
    # min_date = current_time.strftime('%Y-%m-%d')
    # max_date = end_date.strftime('%Y-%m-%d')
    
    if request.method == "POST":
        date_form = AppointmentDateForm(request.POST)
        if date_form.is_valid():
            appointment_date = date_form.cleaned_data['appointment_date']
            formatted_date = appointment_date.strftime('%Y-%m-%d')
            
            if formatted_date:
                return redirect('book-appointment-doctor' , appointment_date = formatted_date)

    return render(request,'DentalCare/appointment_date_doctor.html',{'date_form':date_form})

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def book_appointment_doctor(request,appointment_date):
    appointment_date = request.GET.get('appointment_date',appointment_date)
    appointment_date_formatted = datetime.strptime(appointment_date, '%Y-%m-%d').date()
    specified_time_slots = [
        '10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', 
        '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM',
        '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM',
        '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM'
    ]

    existing_appointments = Appointment.objects.filter(AppointmentDate=appointment_date_formatted).values_list('TimeSlot',flat = True)
    print(existing_appointments)

    formatted_time_slots = [time_obj.strftime('%I:%M %p') for time_obj in existing_appointments]
    print(formatted_time_slots)

    available_time_slots = [time_slot for time_slot in specified_time_slots if time_slot not in formatted_time_slots]
    print(available_time_slots)

    patients = Patient.objects.all()
    patient_name = []
    for patient in patients:
        patient_name.append(f"{patient.user.first_name} {patient.user.last_name}") 
    print(patient_name)

    if request.method == "POST":
        appointment_form = BookAppointment(request.POST)

        print(appointment_form.errors)
        if appointment_form.is_valid():
            print(appointment_form.errors)

            # appointment_date = request.POST.get('appointment_date')
            appointment_time = request.POST.get('appointment_time')

        
            adjusted_appointment_time = appointment_time.replace(" AM", ":00").replace(" PM", ":00")

            
            patient = request.POST.get('patient')
            patient = patient.split()
            first_name , last_name = patient
            
            patient = Patient.objects.filter(user__first_name = first_name, user__last_name = last_name).first()
            print(patient)

            symptoms = appointment_form.cleaned_data['symptoms']
            # print(symptoms)
            department_name = assign_doctor(symptoms)
            # print(department_name)
            doctor = Doctor.objects.filter(department=department_name).first()
            # print(doctor)
            
            
            if doctor:
                # print("Y")
                patient_appointment = Appointment(
                    patient = patient,
                    doctor = doctor ,
                    AppointmentDate = appointment_date,
                    TimeSlot = adjusted_appointment_time, 
                    symptoms = symptoms)
                
                
                patient_appointment.save()

                phone_number_str = patient.mobile.as_e164

                send_sms(phone_number_str, f"Hello, {patient.user.first_name}, You appointment with OralFix Dental Care has been scheduled for {appointment_date} and {appointment_time}. Your Attending Doctor is Dr. {doctor.get_name}.Please arrive 10 minutes before your scheduled appointment time.If you have any questions or need to reschedule, please contact the Doctor at {doctor.mobile}.")

                messages.success(request, "Appointment Booked Successfully!")


                return redirect('view-appointment-doctor') 
            else:
                print(appointment_form.errors)
                return render(request, 'DentalCare/book-appointment-doctor.html', {'appointment_form': appointment_form, 'error': 'No doctor available' , 'appointment_date' : appointment_date })
            
    else:
        appointment_form = BookAppointment()

    return render(request, 'DentalCare/book-appointment-doctor.html', {'appointment_date': appointment_date , 'available_time_slots': available_time_slots , 'appointment_form' : appointment_form , 'patient_name' : patient_name} )

@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def view_all_appointment_doctor(request):
    doctor = Doctor.objects.get(user_id=request.user.id)

    appointments=Appointment.objects.filter(doctor = doctor)
    return render(request,'DentalCare/view_appointments_doctor.html',{'appointments':appointments})


@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def cancel_appointment_doctor(request, appointment_id):

    appointment = Appointment.objects.get(id=appointment_id, doctor__user=request.user)
    appointment.is_canceled = True
    appointment.save()

    doctor = Doctor.objects.get(user_id = request.user.id)
    phone_number_str = doctor.mobile.as_e164
    send_sms(phone_number_str, 'Your Appointment has been successfully canceled.')
    messages.success(request, "Appointment Cancelled Successfully!")

    return redirect('view-appointment-doctor')


# Add Patient
@login_required(login_url='doctor-login')
@user_passes_test(is_doctor)
def add_patient_doctor(request):
    userForm=PatientUserForm()
    patientForm=PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=PatientUserForm(request.POST)
        patientForm=PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save(commit=False)
            
            username = userForm.cleaned_data['first_name'].lower() + str(random.randint(1000, 9999))
            user.username = username
            password = username
            
            user.set_password(password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user

            profile_picture = generate_profile_picture(user)
            patient.profile_picture = profile_picture

            patient.status=True
            patient.save()

            my_patient_group = Group.objects.get(name='PATIENT')
            user.groups.add(my_patient_group)

            phone_number = patientForm.cleaned_data['mobile']
            phone_number_str = phone_number.as_e164

            send_sms(phone_number_str, f"You have been registered to Oral Fix Dental Clinic. Your Username is {user.username} and Password is {password}.")

            messages.success(request,'Patient Profile Added Successfully!')



        return HttpResponseRedirect('doctor-dashboard')
    return render(request,'DentalCare/add-patient-doctor.html',context=mydict)
