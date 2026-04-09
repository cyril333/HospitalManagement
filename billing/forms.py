from django import forms
from .models import Billing

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'admission', 'consultation', 'prescription', 'subtotal', 'discount', 'total_amount', 'payment_status', 'bill_date']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
        }