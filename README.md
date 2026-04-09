# HospitalManagement - Django Project

A web-based Hospital Management System built with Django and MySQL. This project was developed as a group assignment, with each app representing a specific module of the system.

***

## Project Structure

    HospitalManagement/
    ├── accounts/
    │   ├── migrations/
    │   ├── templates/accounts/
    │   │   ├── doctor_list.html
    │   │   ├── nurse_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── admissions/
    │   ├── migrations/
    │   ├── templates/admissions/
    │   │   ├── admission_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── billing/
    │   ├── migrations/
    │   ├── templates/billing/
    │   │   ├── billing_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── consultations/
    │   ├── migrations/
    │   ├── templates/consultations/
    │   │   ├── consultation_list.html
    │   │   ├── prescription_list.html
    │   │   ├── medical_record_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── departments/
    │   ├── migrations/
    │   ├── templates/departments/
    │   │   ├── department_list.html
    │   │   ├── room_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── inventory/
    │   ├── migrations/
    │   ├── templates/inventory/
    │   │   ├── inventory_home.html
    │   │   ├── medicine_list.html
    │   │   ├── medicine_form.html
    │   │   ├── supplies_list.html
    │   │   ├── supplies_form.html
    │   │   └── confirm_delete.html
    │   ├── admin.py
    │   ├── apps.py
    │   ├── forms.py
    │   ├── models.py
    │   ├── urls.py
    │   └── views.py
    ├── patients/
    │   ├── migrations/
    │   ├── templates/patients/
    │   │   ├── patient_list.html
    │   │   ├── form.html
    │   │   └── confirm_delete.html
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
    ├── manage.py
    ├── requirements.txt
    ├── .gitignore
    └── README.md

***

## Requirements

- Python 3.x
- Django 4.2
- MySQL / MariaDB 10.4+
- mysqlclient

***

## How to Set Up and Run

### 1. Clone the Repository

    git clone <your-repository-url>
    cd HospitalManagement

### 2. Install Dependencies

    pip install -r requirements.txt

If requirements.txt is not present, install manually:

    pip install Django==4.2 mysqlclient

### 3. Configure the Database

Open hospital_project/settings.py and update the DATABASES section:

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

Make sure the database is already created in MySQL before running migrations.

### 4. Apply Migrations (run in this order)

    python manage.py makemigrations departments
    python manage.py makemigrations accounts
    python manage.py makemigrations patients
    python manage.py makemigrations inventory
    python manage.py makemigrations consultations
    python manage.py makemigrations admissions
    python manage.py makemigrations billing
    python manage.py migrate

### 5. Create a Superuser (Admin Account)

    python manage.py createsuperuser

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

    python manage.py runserver 8080

The project will be accessible at: http://127.0.0.1:8080

Admin panel: http://127.0.0.1:8080/admin

***

## App Descriptions

| App           | Description                                                   |
|---------------|---------------------------------------------------------------|
| accounts      | Handles user authentication, login, doctors, and nurses       |
| admissions    | Manages patient admissions and discharge records              |
| billing       | Tracks billing, payments, and invoices                        |
| consultations | Records doctor consultations, prescriptions, medical records  |
| departments   | Manages hospital departments and rooms                        |
| inventory     | Tracks medicines and hospital supplies                        |
| patients      | Stores and manages patient information and records            |

***

## Module URLs

| Module        | URL                          |
|---------------|------------------------------|
| Home          | /                            |
| Login         | /login/                      |
| Admin Panel   | /admin/                      |
| Accounts      | /accounts/doctors/           |
|               | /accounts/nurses/            |
| Departments   | /departments/                |
|               | /departments/rooms/          |
| Patients      | /patients/                   |
| Admissions    | /admissions/                 |
| Consultations | /consultations/              |
|               | /consultations/prescriptions/|
|               | /consultations/records/      |
| Billing       | /billing/                    |
| Inventory     | /inventory/                  |
|               | /inventory/medicines/        |
|               | /inventory/supplies/         |

***

## Resetting Migrations (if needed)

If you encounter migration conflicts, follow these steps:

1. Delete all migration files except __init__.py in each app's migrations/ folder:

    del /s /q accounts\migrations\0*.py
    del /s /q admissions\migrations\0*.py
    del /s /q billing\migrations\0*.py
    del /s /q consultations\migrations\0*.py
    del /s /q departments\migrations\0*.py
    del /s /q inventory\migrations\0*.py
    del /s /q patients\migrations\0*.py

2. Drop and recreate your database in MySQL Workbench.

3. Re-run makemigrations in order (see Step 4 above).

***

## Group Members

**Group 5**

- Abesia, Ian - Accounts, Departments
- Antolijao, Ave Cyril G. - Consultations, Admissions
- Jabines, Synd T. - Patients
- Lanticse, Vince Clark B. — Inventory App
- Lariosa, Allen N. - Billing

***

## Notes

- This project uses Django 4.2 for compatibility with MySQL/MariaDB 10.4.
- Ensure MySQL service is running before starting the server.
- Do not set AUTH_USER_MODEL in settings.py — the project uses Django's built-in User model.
- The .env file (if used) is excluded from version control for security.