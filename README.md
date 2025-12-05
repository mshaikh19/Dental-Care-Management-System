# 🦷 Dental Care Management System

A comprehensive web-based dental clinic management system built with **Django** to automate and streamline dental clinic operations, patient management, and appointment scheduling.

---

## About

The Dental Care Management System is designed to overcome manual system limitations by introducing a fully automated, web-based solution. It provides structured management of patient records, doctor profiles, and appointments with role-based access for **Admins**, **Doctors**, and **Patients**.

Developed By: Shaikh Maryam Mohammed Farooq
Institution: Gujarat University
Program: M.Sc. IT (Software Development - Web & Mobile Application)
Semester: 4 (Batch: 2022–2025)

yaml
Copy code

---

## Features

### Administrator
- Full system control and secure access
- Manage patients and doctor profiles (CRUD)
- View and control all clinic appointments
- Create login credentials for doctors
- Access advanced dashboard analytics

### Doctor
- Secure login provided by the administrator
- Add/view patient records
- Schedule and manage appointments
- Update personal profile

### Patient
- Self-registration and secure login
- Book appointments with preferred doctors
- View booking history
- Edit profile and personal details

### System Highlights
- Automated notification messages
- Real-time appointment booking
- Role-based access and secure password handling
- Profile image upload support

---

## Technologies Used

### Frontend
- HTML5  
- CSS3  
- Bootstrap  
- JavaScript  

### Backend
- Python 3.8+
- Django Framework
- Django ORM
- Django Authentication & Forms

### Database
- SQLite3 (default)

---

## Configuration & Setup

### Prerequisites
Python 3.8 or higher

pip package manager

Virtual environment (recommended)

### Installation

#### Clone the Repository
```
git clone https://github.com/mshaikh19/Dental-Care-Management-System.git
cd Dental-Care-Management-System
```

#### Create & Activate Virtual Environment
```

python -m venv venv


#Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

```

#### Install Dependencies

```
pip install django pillow
```
#### Setup Database
```
python manage.py makemigrations
python manage.py migrate
```

#### Create Superuser
```
python manage.py createsuperuser
```
#### Run the Development Server
```
python manage.py runserver
```
Application runs on: http://127.0.0.1:8000/

### Usage
Access Points

Admin	
  http://127.0.0.1:8000/admin/	
  Manage doctors, patients, and appointments
  
Main App	
  http://127.0.0.1:8000/	
  Patient/Doctor portal and registration

### Database Configuration
Located in: DentalCareManagementSystem/settings.py

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Media Files
```
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media/profile_pics/')
```

## Screenshots (Optional Section Placeholder)

Login Page	
  Secure authentication for all users
Patient Dashboard	
  Appointment history and profile management
Admin Panel	
  Complete management control
Doctor Panel	
  Patient and appointment tracking

## License

This project is open source and available under the MIT License.

```
MIT License

Copyright (c) 2024 Shaikh Maryam Mohammed Farooq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

## Acknowledgements

This project was created as part of the M.Sc. IT program at Gujarat University (2024).

Special appreciation to: 
  Department of Animation, ITIMS & Mobile Applications
  Django Community

## Contact
  Developer: Shaikh Maryam Mohammed Farooq
  Gujarat University | M.Sc. IT | Semester 4


Made with ❤️ dedication for better healthcare digitalization | 2024

