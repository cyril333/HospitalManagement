from django.contrib import admin
from .models import Admission, AdmissionSupplyUsage

@admin.register(Admission)
class AdmissionAdmin(admin.ModelAdmin):
    list_display = ('admission_id', 'patient', 'room', 'attending_doctor', 'admitted_in', 'status')
    search_fields = ('patient__patient_name',)

@admin.register(AdmissionSupplyUsage)
class AdmissionSupplyUsageAdmin(admin.ModelAdmin):
    list_display = ('usage_id', 'admission', 'supply', 'quantity_used', 'unit_cost', 'line_total', 'used_date')