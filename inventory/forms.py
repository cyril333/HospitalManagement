from django import forms
from .models import InventoryMedicine, Supplies

class InventoryMedicineForm(forms.ModelForm):
    class Meta:
        model = InventoryMedicine
        fields = ['medicine_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SuppliesForm(forms.ModelForm):
    class Meta:
        model = Supplies
        fields = ['supply_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }