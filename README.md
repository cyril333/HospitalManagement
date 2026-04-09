# HospitalManagement - Django Project

A web-based Hospital Inventory Management System built with Django and MySQL. This project was developed as a group assignment, with each app representing a specific module of the system.

***

## Project Structure

    HospitalManagement/
    ├── accounts/           # User authentication and login
    ├── admissions/         # Patient admission management
    ├── billing/            # Billing and payment records
    ├── consultations/      # Doctor consultations and prescriptions
    ├── departments/        # Hospital departments
    ├── inventory/          # Medical inventory management
    │   ├── models.py       # InventoryMedicine and Supplies models
    │   ├── views.py        # Inventory, medicine, and supplies views
    │   ├── urls.py         # Inventory URL routes
    │   ├── forms.py        # Medicine and supplies forms
    │   └── admin.py        # Admin panel registration
    ├── patients/           # Patient records
    ├── hospital_project/   # Main project settings and URLs
    ├── templates/
    │   ├── base.html               # Base template
    │   ├── index.html              # Home/index page
    │   ├── login.html              # Login page
    │   └── inventory/
    │       ├── inventory_home.html # Inventory landing page
    │       ├── medicine_list.html  # Medicine inventory list
    │       ├── medicine_form.html  # Add/edit medicine form
    │       ├── supplies_list.html  # Supplies inventory list
    │       ├── supplies_form.html  # Add/edit supply form
    │       └── confirm_delete.html # Delete confirmation page
    ├── manage.py
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

If `requirements.txt` is not present, install manually:

    pip install Django==4.2 mysqlclient

### 3. Configure the Database

Open `hospital_project/settings.py` and update the `DATABASES` section with your MySQL credentials:

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

### 4. Apply Migrations

    python manage.py makemigrations
    python manage.py migrate

### 5. Create a Superuser (Admin Account)

    python manage.py createsuperuser

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

    python manage.py runserver 8080

The project will be accessible at: **http://127.0.0.1:8080**

Admin panel: **http://127.0.0.1:8080/admin**

***

## App Descriptions

| App | Description |
|---|---|
| `accounts` | Handles user authentication, login, and user roles |
| `admissions` | Manages patient admissions and discharge records |
| `billing` | Tracks billing, payments, and invoices |
| `consultations` | Records doctor consultations and prescriptions |
| `departments` | Manages hospital departments and assignments |
| `inventory` | Tracks medical supplies and equipment (medicines & supplies) |
| `patients` | Stores and manages patient information and records |

***

## Inventory Module URLs

| URL | Description |
|---|---|
| `/inventory/` | Inventory landing page |
| `/inventory/medicines/` | Medicine inventory list |
| `/inventory/medicines/add/` | Add new medicine |
| `/inventory/medicines/edit/<id>/` | Edit medicine |
| `/inventory/medicines/delete/<id>/` | Delete medicine |
| `/inventory/supplies/` | Supplies inventory list |
| `/inventory/supplies/add/` | Add new supply |
| `/inventory/supplies/edit/<id>/` | Edit supply |
| `/inventory/supplies/delete/<id>/` | Delete supply |

***

## Group Members

**Group 5**

- Abesia, Ian
- Antolijao, Ave Cyril G.
- Jabines, Synd T.
- Lanticse, Vince Clark B. — Inventory App
- Lariosa, Allen N.

***

## Notes

- This project uses Django 4.2 for compatibility with MySQL/MariaDB 10.4.
- Ensure MySQL service is running before starting the server.
- The `.env` file (if used) is excluded from version control for security.