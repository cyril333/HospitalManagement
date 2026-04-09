from django import forms
from django.contrib.auth.models import User
from .models import DoctorProfile, NurseProfile

class DoctorForm(forms.ModelForm):
    class Meta:
        model = DoctorProfile
        fields = ['user', 'department', 'specialization', 'license_number', 'contact_number', 'daily_rate']

class NurseForm(forms.ModelForm):
    class Meta:
        model = NurseProfile
        fields = ['user', 'department', 'shift_schedule', 'contact_number']