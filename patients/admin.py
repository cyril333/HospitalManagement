from django.contrib import admin
from .models import Patient

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('patient_id', 'patient_name', 'dateofbirth', 'age', 'status')
    search_fields = ('patient_name',)