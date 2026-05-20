from django.contrib import admin
from .models import Billing

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'patient', 'total_amount', 'payment_status', 'bill_date')
    search_fields = ('patient__patient_name',)