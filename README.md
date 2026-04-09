# HospitalManagement - Django Project

A web-based Hospital Management System built with Django and MySQL. This project was developed as a group assignment, with each app representing a specific module of the system.

---

## Project Structure

```
HospitalManagement/
├── accounts/           # User authentication and login
├── admissions/         # Patient admission management
├── billing/            # Billing and payment records
├── consultations/      # Doctor consultations and prescriptions
├── departments/        # Hospital departments
├── inventory/          # Medical inventory management
├── patients/           # Patient records
├── hospital_project/   # Main project settings and URLs
├── templates/
│   ├── base.html       # Base template
│   ├── index.html      # Home/index page
│   └── login.html      # Login page
├── manage.py
├── .gitignore
└── README.md
```

---

## Requirements

- Python 3.x
- Django 4.2
- MySQL / MariaDB 10.4+
- mysqlclient

---

## How to Set Up and Run

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd HospitalManagement
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

> If `requirements.txt` is not present, install manually:
> ```bash
> pip install Django==4.2 mysqlclient
> ```

### 3. Configure the Database

Open `hospital_project/settings.py` and update the `DATABASES` section with your MySQL credentials:

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

Make sure the database is already created in MySQL before running migrations.

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver 8080
```

The project will be accessible at: **http://127.0.0.1:8080**

Admin panel: **http://127.0.0.1:8080/admin**

---

## App Descriptions

| App | Description |
|---|---|
| `accounts` | Handles user authentication, login, and user roles |
| `admissions` | Manages patient admissions and discharge records |
| `billing` | Tracks billing, payments, and invoices |
| `consultations` | Records doctor consultations and prescriptions |
| `departments` | Manages hospital departments and assignments |
| `inventory` | Tracks medical supplies and equipment |
| `patients` | Stores and manages patient information and records |

---

## Group Members

- Group 5 (5 members)

- Abesia, Ian
- Antolijao, Ave Cyril G.
- Jabines, Synd T.
- Lanticse, Vince Clark B.
- Lariosa, Allen N.



## Notes

- This project uses Django 4.2 for compatibility with MySQL/MariaDB 10.4.
- Ensure MySQL service is running before starting the server.
- The `.env` file (if used) is excluded from version control for security.
