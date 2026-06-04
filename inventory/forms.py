from django import forms
from django.core.exceptions import ValidationError
from .models import InventoryMedicine, Supplies


MEDICINE_CATEGORY_CHOICES = [
    ('Antibiotic', 'Antibiotic'),
    ('Analgesic', 'Analgesic'),
    ('Antipyretic', 'Antipyretic'),
    ('Antiseptic', 'Antiseptic'),
    ('Vitamin', 'Vitamin'),
    ('Syrup', 'Syrup'),
    ('Tablet', 'Tablet'),
    ('Capsule', 'Capsule'),
    ('Injection', 'Injection'),
    ('Other', 'Other'),
]

SUPPLY_CATEGORY_CHOICES = [
    ('PPE', 'PPE'),
    ('Bandage', 'Bandage'),
    ('Syringe', 'Syringe'),
    ('Gloves', 'Gloves'),
    ('Cotton', 'Cotton'),
    ('Disinfectant', 'Disinfectant'),
    ('IV Supply', 'IV Supply'),
    ('Cleaning Supply', 'Cleaning Supply'),
    ('Other', 'Other'),
]

UNIT_CHOICES = [
    ('piece', 'Piece'),
    ('box', 'Box'),
    ('bottle', 'Bottle'),
    ('pack', 'Pack'),
    ('tablet', 'Tablet'),
    ('capsule', 'Capsule'),
    ('ml', 'mL'),
    ('mg', 'mg'),
    ('liter', 'Liter'),
    ('set', 'Set'),
]


class BaseStyledForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css = 'form-control'
            if isinstance(field.widget, forms.DateInput):
                css += ' date-input'
            field.widget.attrs['class'] = css


class InventoryMedicineForm(BaseStyledForm):
    category = forms.ChoiceField(choices=MEDICINE_CATEGORY_CHOICES)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)

    class Meta:
        model = InventoryMedicine
        fields = ['medicine_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError('Quantity cannot be less than zero.')
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price is not None and unit_price < 0:
            raise ValidationError('Unit price cannot be negative.')
        return unit_price


class SuppliesForm(BaseStyledForm):
    category = forms.ChoiceField(choices=SUPPLY_CATEGORY_CHOICES)
    unit = forms.ChoiceField(choices=UNIT_CHOICES)

    class Meta:
        model = Supplies
        fields = ['supply_name', 'category', 'quantity', 'unit', 'expiry_date', 'unit_price']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'quantity': forms.NumberInput(attrs={'min': 0}),
            'unit_price': forms.NumberInput(attrs={'min': 0, 'step': '0.01'}),
        }

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise ValidationError('Quantity cannot be less than zero.')
        return quantity

    def clean_unit_price(self):
        unit_price = self.cleaned_data.get('unit_price')
        if unit_price is not None and unit_price < 0:
            raise ValidationError('Unit price cannot be negative.')
        return unit_price