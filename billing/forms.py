from django import forms
from .models import Billing
from django.contrib.auth.models import User

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient', 'admission', 'consultation', 'prescription', 'subtotal', 'discount', 'total_amount', 'payment_status', 'bill_date']
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
        }

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']