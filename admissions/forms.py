from django import forms
from .models import Admission, AdmissionSupplyUsage

class AdmissionForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'room', 'attending_doctor', 'admitted_in', 'admitted_out', 'status', 'remarks']
        widgets = {
            'admitted_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'admitted_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class AdmissionSupplyUsageForm(forms.ModelForm):
    class Meta:
        model = AdmissionSupplyUsage
        fields = ['admission', 'supply', 'quantity_used', 'unit_cost', 'line_total', 'used_date']
        widgets = {
            'used_date': forms.DateInput(attrs={'type': 'date'}),
        }