from django.contrib import admin
from .models import Consultation, MedicalRecord, Prescription, PrescriptionItem

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('consultation_id', 'patient', 'doctor', 'consultation_date', 'status')
    search_fields = ('patient__patient_name',)

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'patient', 'doctor', 'diagnosis', 'record_date')

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_id', 'patient', 'doctor', 'prescription_date', 'total_items')

@admin.register(PrescriptionItem)
class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('prescription_item_id', 'prescription', 'medicine', 'quantity', 'dosage', 'line_total')