from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Doctor', 'Doctor'),
        ('Nurse', 'Nurse'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    created_by_admin = models.ForeignKey(
        'AdminProfile',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='created_users'
    )

    def __str__(self):
        return f"{self.user.username} ({self.role})"


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    access_level = models.CharField(max_length=100, default='Full Access')
    last_login = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username


class DoctorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    department = models.ForeignKey('departments.Department', on_delete=models.PROTECT)
    specialization = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True)
    contact_number = models.CharField(max_length=20)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.daily_rate is not None and self.daily_rate < 0:
            raise ValidationError({'daily_rate': 'Daily rate cannot be negative.'})

    def __str__(self):
        full_name = self.user.get_full_name().strip()
        return full_name if full_name else self.user.username


class NurseProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='nurse_profile')
    department = models.ForeignKey('departments.Department', on_delete=models.PROTECT)
    shift_schedule = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=20)

    def __str__(self):
        full_name = self.user.get_full_name().strip()
        return full_name if full_name else self.user.username