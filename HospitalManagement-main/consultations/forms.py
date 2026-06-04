from django import forms
from .models import Consultation, MedicalRecord, Prescription, PrescriptionItem
from inventory.models import InventoryMedicine


class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = [
            'patient',
            'doctor',
            'prescription',
            'consultation_date',
            'consultation_time',
            'status',
            'remarks'
        ]
        widgets = {
            'consultation_date': forms.DateInput(attrs={'type': 'date'}),
            'consultation_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['prescription'].required = False
        self.fields['prescription'].empty_label = 'Select Prescription'
        self.fields['prescription'].queryset = Prescription.objects.select_related(
            'patient', 'doctor'
        ).order_by('-prescription_date', '-prescription_id')

        patient_id = None

        if self.is_bound:
            patient_id = self.data.get('patient')
        elif self.instance and self.instance.pk:
            patient_id = self.instance.patient_id

        if patient_id:
            self.fields['prescription'].queryset = Prescription.objects.filter(
                patient_id=patient_id
            ).select_related('patient', 'doctor').order_by('-prescription_date', '-prescription_id')


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
        fields = ['prescription', 'medicine', 'quantity', 'unit_price']
        labels = {
            'unit_price': 'Total Price',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        medicines = InventoryMedicine.objects.all().order_by('medicine_name')
        self.fields['medicine'].queryset = medicines
        self.fields['medicine'].empty_label = 'Select Medicine'

        choices = [('', 'Select Medicine')]
        for med in medicines:
            choices.append((med.pk, f"{med.medicine_name} (Stock: {med.quantity})"))

        self.fields['medicine'].widget = forms.Select(choices=choices)

        self.fields['unit_price'].required = False
        self.fields['unit_price'].widget.attrs['readonly'] = True

        if self.instance and self.instance.pk and self.instance.unit_price is not None:
            self.fields['unit_price'].initial = self.instance.unit_price

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity <= 0:
            raise forms.ValidationError('Quantity must be greater than zero.')
        return quantity

    def clean(self):
        cleaned_data = super().clean()
        medicine = cleaned_data.get('medicine')
        quantity = cleaned_data.get('quantity')

        if medicine and quantity:
            available_stock = medicine.quantity

            if self.instance and self.instance.pk:
                if self.instance.medicine_id == medicine.pk:
                    available_stock += self.instance.quantity

            if quantity > available_stock:
                self.add_error(
                    'quantity',
                    f'Only {available_stock} item(s) available in stock for {medicine.medicine_name}.'
                )

            cleaned_data['unit_price'] = medicine.unit_price * quantity

        return cleaned_data

    def save(self, commit=True):
        item = super().save(commit=False)

        old_medicine = None
        old_quantity = 0

        if self.instance and self.instance.pk:
            old_item = PrescriptionItem.objects.get(pk=self.instance.pk)
            old_medicine = old_item.medicine
            old_quantity = old_item.quantity

        if item.medicine:
            item.unit_price = item.medicine.unit_price * item.quantity

        if commit:
            if old_medicine:
                old_medicine.quantity += old_quantity
                old_medicine.save(update_fields=['quantity'])

            item.medicine.quantity -= item.quantity
            item.medicine.save(update_fields=['quantity'])

            item.save()

            prescription = item.prescription
            prescription.total_items = prescription.prescriptionitem_set.count()
            prescription.save(update_fields=['total_items'])

        return item