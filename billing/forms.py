from django import forms
from .models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'admission', 'consultation', 'prescription', 'subtotal', 'discount', 'payment_status', 'bill_date']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        subtotal = cleaned_data.get('subtotal')
        discount = cleaned_data.get('discount')
        if subtotal is not None and discount is not None and discount > subtotal:
            raise forms.ValidationError('Discount cannot exceed subtotal.')
        return cleaned_data