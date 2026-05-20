from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = [
            'patient_name', 'gender', 'dateofbirth',
            'blood_type', 'contact_number', 'address',
            'emergency_contact_name', 'emergency_contact_number',
            'status'
        ]
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'type': 'date', 'id': 'id_dateofbirth'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }