from decimal import Decimal
from django import forms
from .models import Billing
from admissions.models import Admission
from consultations.models import Consultation, Prescription


class BillingForm(forms.ModelForm):
    subtotal = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        disabled=True
    )

    total_amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        disabled=True
    )

    admitted_out = forms.DateTimeField(
        required=False,
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        help_text='Required when marking the bill as Paid for an active admission.'
    )

    class Meta:
        model = Billing
        fields = [
            'patient',
            'admission',
            'consultation',
            'prescription',
            'discount',
            'payment_status',
            'bill_date'
        ]
        widgets = {
            'bill_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'discount': 'Discount (%)',
            'admitted_out': 'Discharge Date & Time',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.order_fields([
            'patient',
            'admission',
            'consultation',
            'prescription',
            'admitted_out',
            'subtotal',
            'discount',
            'total_amount',
            'payment_status',
            'bill_date',
        ])

        patient_id = None

        if self.is_bound:
            patient_id = self.data.get('patient')
        elif self.instance and self.instance.pk:
            patient_id = self.instance.patient_id

        self.fields['admission'].queryset = Admission.objects.select_related(
            'patient', 'attending_doctor', 'room'
        ).order_by('-admission_id')

        self.fields['consultation'].queryset = Consultation.objects.select_related(
            'patient', 'doctor'
        ).order_by('-consultation_date', '-consultation_id')

        self.fields['prescription'].queryset = Prescription.objects.select_related(
            'patient', 'doctor'
        ).order_by('-prescription_date', '-prescription_id')

        if patient_id:
            self.fields['admission'].queryset = self.fields['admission'].queryset.filter(patient_id=patient_id)
            self.fields['consultation'].queryset = self.fields['consultation'].queryset.filter(patient_id=patient_id)
            self.fields['prescription'].queryset = self.fields['prescription'].queryset.filter(patient_id=patient_id)

        if self.instance and self.instance.pk:
            self.fields['subtotal'].initial = self.instance.subtotal
            self.fields['total_amount'].initial = self.instance.total_amount

            if self.instance.admission and self.instance.admission.admitted_out:
                self.fields['admitted_out'].initial = self.instance.admission.admitted_out.strftime('%Y-%m-%dT%H:%M')
        else:
            self.fields['subtotal'].initial = Decimal('0.00')
            self.fields['total_amount'].initial = Decimal('0.00')

    def clean_discount(self):
        discount = self.cleaned_data.get('discount')
        if discount is not None:
            if discount < Decimal('0'):
                raise forms.ValidationError('Discount percentage cannot be negative.')
            if discount > Decimal('100'):
                raise forms.ValidationError('Discount percentage cannot be greater than 100.')
        return discount

    def clean(self):
        cleaned_data = super().clean()

        patient = cleaned_data.get('patient')
        admission = cleaned_data.get('admission')
        consultation = cleaned_data.get('consultation')
        prescription = cleaned_data.get('prescription')
        discount = cleaned_data.get('discount') or Decimal('0.00')
        payment_status = cleaned_data.get('payment_status') or 'Unpaid'
        admitted_out = cleaned_data.get('admitted_out')

        if patient and admission and patient != admission.patient:
            self.add_error('admission', 'Selected admission does not belong to the selected patient.')

        if patient and consultation and patient != consultation.patient:
            self.add_error('consultation', 'Selected consultation does not belong to the selected patient.')

        if patient and prescription and patient != prescription.patient:
            self.add_error('prescription', 'Selected prescription does not belong to the selected patient.')

        if payment_status == 'Paid' and admission:
            if admission.status == 'Active' and not admitted_out:
                self.add_error('admitted_out', 'Discharge date and time is required before marking this admission bill as Paid.')

            if admitted_out and admission.admitted_in and admitted_out <= admission.admitted_in:
                self.add_error('admitted_out', 'Discharge date and time must be later than admitted in.')

        bill = Billing(
            patient=patient,
            admission=admission,
            consultation=consultation,
            prescription=prescription,
            discount=discount,
            payment_status=payment_status,
            bill_date=cleaned_data.get('bill_date')
        )

        if admission and admitted_out:
            original_admitted_out = admission.admitted_out
            original_status = admission.status

            admission.admitted_out = admitted_out
            admission.status = 'Discharged'

            cleaned_data['subtotal'] = bill.calculate_subtotal().quantize(Decimal('0.01'))
            cleaned_data['total_amount'] = bill.calculate_total_amount().quantize(Decimal('0.01'))

            admission.admitted_out = original_admitted_out
            admission.status = original_status
        else:
            cleaned_data['subtotal'] = bill.calculate_subtotal().quantize(Decimal('0.01'))
            cleaned_data['total_amount'] = bill.calculate_total_amount().quantize(Decimal('0.01'))

        return cleaned_data

    def save(self, commit=True):
        bill = super().save(commit=False)
        bill.subtotal = self.cleaned_data.get('subtotal', Decimal('0.00'))
        bill.total_amount = self.cleaned_data.get('total_amount', Decimal('0.00'))

        admission = self.cleaned_data.get('admission')
        admitted_out = self.cleaned_data.get('admitted_out')
        payment_status = self.cleaned_data.get('payment_status')

        if commit:
            if admission and payment_status == 'Paid' and admitted_out:
                admission.admitted_out = admitted_out
                admission.status = 'Discharged'
                admission.save()

            bill.save()

        return bill