"""
URL configuration for DentalCareManagementSystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import path, reverse_lazy

from DentalCare import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page_view,name = 'home_page'),
    path('afterlogin', views.afterlogin_view,name='afterlogin'),

    # For LogIn Page
    path('admin-login-page', views.admin_view_afterlogin),
    path('doctor-login-page', views.doctor_view_afterlogin),
    path('patient-login-page', views.patient_view_afterlogin),

    # For SignUp (Only Patients Can SignUp)
    path('patient-signup', views.patient_signup_view),

    # For LogIn 
    path('admin-login', LoginView.as_view(template_name='DentalCare/adminlogin.html')),
    path('doctor-login', LoginView.as_view(template_name='DentalCare/doctorlogin.html')),
    # path('patient-login', LoginView.as_view(template_name='DentalCare/patientlogin.html') , name='patient-login'),
    path('patient-login', views.custom_login_view, name="patient-login"),


    # For appointments
    path('book-appointment/date/',views.book_appointment_date,name='appointment-date'),
    path('book-appointment/<str:appointment_date>/',views.book_appointment,name='book-appointment'),

    # For logout
    # path('logout/', LogoutView.as_view(template_name='DentalCare/index.html'),name='logout'),
    path('logout/', views.logout_view , name='logout'),

    # For patient
    path('patient-dashboard/', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-view-appointment', views.patient_view_appointment,name='patient-view-appointment'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),

    # For admin dashboard
    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('view-doctor', views.view_doctor,name='view-doctor'),
    path('add-doctor', views.add_doctor,name='add-doctor'),
    path('update-doctor/<int:pk>', views.update_doctor,name='update-doctor'),
    path('delete-doctor/<int:pk>', views.delete_doctor,name='delete-doctor'),
    path('doctor-profile/<int:doctor_id>/', views.doctor_profile_view, name='doctor_profile'),
    
    path('view-patient', views.view_patient,name='view-patient'),
    path('delete-patient/<int:pk>', views.delete_patient,name='delete-patient'),
    path('update-patient/<int:pk>', views.update_patient,name='update-patient'),
    path('patient-profile/<int:patient_id>/', views.patient_profile_view, name='patient_profile'),
    path('add-patient', views.add_patient,name='add-patient'),
    # path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    # path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    # path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    # path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    # path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    # path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),

    path('book-appointment-admin/date/',views.book_appointment_date_admin,name='appointment-date-admin'),
    path('book-appointment-admin/<str:appointment_date>/',views.book_appointment_admin,name='book-appointment-admin'),
    path('view-appointment', views.view_all_appointment,name='view-appointment'),

    path('doctor-dashboard/', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('book-appointment-doctor/date/',views.book_appointment_date_doctor,name='appointment-date-doctor'),
    path('book-appointment-doctor/<str:appointment_date>/',views.book_appointment_doctor,name='book-appointment-doctor'),
    path('view-appointment-doctor', views.view_all_appointment_doctor,name='view-appointment-doctor'),
    path('cancel-appointment-doctor/<int:appointment_id>/', views.cancel_appointment_doctor, name='cancel_appointment_doctor'),
    path('add-patient-doctor', views.add_patient_doctor,name='add-patient-doctor'),



]

from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
