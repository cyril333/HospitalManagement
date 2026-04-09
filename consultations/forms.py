from django import forms
from .models import Consultation, MedicalRecord, Prescription, PrescriptionItem

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = ['patient', 'doctor', 'consultation_date', 'consultation_time', 'status', 'remarks']
        widgets = {
            'consultation_date': forms.DateInput(attrs={'type': 'date'}),
            'consultation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['patient', 'doctor', 'diagnosis', 'notes', 'record_date']
        widgets = {
            'record_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['patient', 'doctor', 'prescription_date', 'total_items', 'remarks']
        widgets = {
            'prescription_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PrescriptionItemForm(forms.ModelForm):
    class Meta:
        model = PrescriptionItem
        fields = ['prescription', 'medicine', 'quantity', 'dosage', 'unit_price', 'line_total']