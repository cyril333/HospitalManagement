from django.contrib import admin
from .models import InventoryMedicine, Supplies

@admin.register(InventoryMedicine)
class InventoryMedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_id', 'medicine_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price')
    search_fields = ('medicine_name', 'category')

@admin.register(Supplies)
class SuppliesAdmin(admin.ModelAdmin):
    list_display = ('supply_id', 'supply_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price')
    search_fields = ('supply_name', 'category')