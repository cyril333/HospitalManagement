from django import forms
from .models import Department, Room

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_name', 'status']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['department', 'room_number', 'room_type', 'status', 'daily_rate']