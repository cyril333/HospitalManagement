from django import forms
from .models import Patient

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'dateofbirth', 'age', 'status']
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'type': 'date'}),
        }