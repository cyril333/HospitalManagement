# MediTrack — Hospital Management System

A web-based Hospital Management System built with **Django 4.2** and **MySQL/MariaDB**, developed as a group project. The system is organized into separate Django apps, with each app representing a major hospital workflow such as accounts, admissions, billing, consultations, departments, inventory, and patients.

---

## Overview

MediTrack is designed to help manage day-to-day hospital operations in one integrated platform. It includes modules for staff management, patient records, consultations, prescriptions, admissions, room handling, billing, and inventory tracking.

The project follows a modular Django structure, making each feature easier to develop and maintain as an independent app. It uses Django templates for the frontend and MySQL as the primary database backend.

---

## Features

- User authentication and role-based access for admin, doctor, and nurse workflows.
- Department and room management with room status and daily rate tracking.
- Patient information management and record handling.
- Consultation, prescription, and medical record management.
- Admission management with room assignment and discharge handling.
- Billing module with subtotal, discount, total amount, and payment status support.
- Inventory tracking for medicines and supplies.

---

## Project Structure

```text
HospitalManagement/
├── accounts/
│   ├── migrations/
│   ├── templates/accounts/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── admissions/
│   ├── migrations/
│   ├── templates/admissions/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── billing/
│   ├── migrations/
│   ├── templates/billing/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── consultations/
│   ├── migrations/
│   ├── templates/consultations/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── departments/
│   ├── migrations/
│   ├── templates/departments/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── inventory/
│   ├── migrations/
│   ├── templates/inventory/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── patients/
│   ├── migrations/
│   ├── templates/patients/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── hospital_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── login.html
├── static/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

This structure reflects the app-based architecture used throughout the project and matches the module separation shown in the current codebase.

---

## Requirements

- Python 3.x
- Django 4.2
- MySQL or MariaDB 10.4+
- `mysqlclient`

The project settings currently target Django with a MySQL backend and include static file support through Django’s built-in `staticfiles` app.

---

## Setup and Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd HospitalManagement
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable or incomplete, install the main dependencies manually:

```bash
pip install Django==4.2 mysqlclient
```

### 3. Configure the database

Open `hospital_project/settings.py` and update the `DATABASES` configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'your_database_name',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Create the database in MySQL before running migrations.

### 4. Apply migrations

```bash
python manage.py makemigrations departments
python manage.py makemigrations accounts
python manage.py makemigrations patients
python manage.py makemigrations inventory
python manage.py makemigrations consultations
python manage.py makemigrations admissions
python manage.py makemigrations billing
python manage.py migrate
```

### 5. Create a superuser

```bash
python manage.py createsuperuser
```

### 6. Run the development server

```bash
python manage.py runserver 8080
```

Application URL: [http://127.0.0.1:8080](http://127.0.0.1:8080)  
Admin panel: [http://127.0.0.1:8080/admin](http://127.0.0.1:8080/admin)

---

## Application Modules

| App | Description |
|---|---|
| `accounts` | Handles authentication, doctor profiles, nurse profiles, and role-related user management. |
| `admissions` | Manages patient admissions, room assignments, discharge flow, and admission supply usage. |
| `billing` | Tracks bills, charge computation, discounts, totals, and payment status. |
| `consultations` | Manages consultations, prescriptions, prescription items, and medical records. |
| `departments` | Manages hospital departments and room records. |
| `inventory` | Tracks medicines and supplies for hospital inventory workflows. |
| `patients` | Stores patient information and patient-related records. |

---

## Main Routes

| Module | URL |
|---|---|
| Home | `/` |
| Login | `/login/` |
| Admin Panel | `/admin/` |
| Doctors | `/accounts/doctors/` |
| Nurses | `/accounts/nurses/` |
| Departments | `/departments/` |
| Rooms | `/departments/rooms/` |
| Patients | `/patients/` |
| Admissions | `/admissions/` |
| Consultations | `/consultations/` |
| Prescriptions | `/consultations/prescriptions/` |
| Medical Records | `/consultations/records/` |
| Billing | `/billing/` |
| Inventory | `/inventory/` |
| Medicines | `/inventory/medicines/` |
| Supplies | `/inventory/supplies/` |

---

## Migration Reset Guide

If migration conflicts occur during development, use the following recovery process carefully:

1. Delete generated migration files in each app’s `migrations/` folder except `__init__.py`.
2. Drop and recreate the development database.
3. Re-run `makemigrations` for each app in dependency order.
4. Run `python manage.py migrate` again.

Example Windows commands:

```bash
del /s /q accounts\migrations\0*.py
del /s /q admissions\migrations\0*.py
del /s /q billing\migrations\0*.py
del /s /q consultations\migrations\0*.py
del /s /q departments\migrations\0*.py
del /s /q inventory\migrations\0*.py
del /s /q patients\migrations\0*.py
```

---

## Group Members

**Group 5**

- Abesia, Ian — Accounts, Departments
- Antolijao, Ave Cyril G. — Consultations, Admissions
- Jabines, Snyd T. — Patients
- Lanticse, Vince Clark B. — Inventory
- Lariosa, Allen N. — Billing

The project presentation identifies this system as a Group 5 hospital inventory and management system proposal with shared business rules and module responsibilities.

---

## Notes

- The project uses Django 4.2 for compatibility with the current backend setup.
- Ensure the MySQL service is running before starting the application.
- The project uses Django’s built-in `User` model rather than a custom `AUTH_USER_MODEL` configuration, based on the shared codebase structure.
- Static assets should be stored in a `static/` directory and served through Django static file settings rather than from the `templates/` folder.