from django.contrib import admin
from .models import Billing

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'patient', 'subtotal', 'discount', 'total_amount', 'payment_status', 'bill_date')
    list_filter = ('payment_status', 'bill_date')
    search_fields = ('patient__first_name', 'patient__last_name', 'bill_id')
    readonly_fields = ('total_amount',)