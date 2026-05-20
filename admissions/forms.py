from django import forms
from .models import Admission, AdmissionSupplyUsage
from billing.models import Billing


class AdmissionCreateForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'room', 'attending_doctor', 'admitted_in', 'status', 'remarks']
        widgets = {
            'admitted_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['admitted_in'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['status'].initial = 'Active'

        if self.instance and self.instance.pk and self.instance.admitted_in:
            self.initial['admitted_in'] = self.instance.admitted_in.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        patient = cleaned_data.get('patient')
        room = cleaned_data.get('room')
        status = cleaned_data.get('status')

        if status == 'Discharged':
            self.add_error('status', 'New admissions cannot be marked as discharged immediately.')

        if room and status == 'Active':
            room_in_use = Admission.objects.filter(
                room=room,
                status='Active'
            ).exists()

            if room_in_use:
                self.add_error('room', 'This room is already occupied by another active admission.')

        if patient and status == 'Active':
            patient_already_active = Admission.objects.filter(
                patient=patient,
                status='Active'
            ).exists()

            if patient_already_active:
                self.add_error('patient', 'This patient already has an active admission.')

        return cleaned_data


class AdmissionEditForm(forms.ModelForm):
    class Meta:
        model = Admission
        fields = ['patient', 'room', 'attending_doctor', 'admitted_in', 'admitted_out', 'status', 'remarks']
        widgets = {
            'admitted_in': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'admitted_out': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['admitted_in'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['admitted_out'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['admitted_out'].required = False
        self.fields['admitted_out'].help_text = 'Required only when status is Discharged.'

        if self.instance and self.instance.pk:
            if self.instance.admitted_in:
                self.initial['admitted_in'] = self.instance.admitted_in.strftime('%Y-%m-%dT%H:%M')
            if self.instance.admitted_out:
                self.initial['admitted_out'] = self.instance.admitted_out.strftime('%Y-%m-%dT%H:%M')

    def clean(self):
        cleaned_data = super().clean()
        admission = self.instance if self.instance and self.instance.pk else None
        patient = cleaned_data.get('patient')
        room = cleaned_data.get('room')
        admitted_in = cleaned_data.get('admitted_in')
        admitted_out = cleaned_data.get('admitted_out')
        status = cleaned_data.get('status')

        if admitted_in and admitted_out and admitted_out <= admitted_in:
            self.add_error('admitted_out', 'Admitted out must be later than admitted in.')

        if status == 'Discharged' and not admitted_out:
            self.add_error('admitted_out', 'Discharge date and time is required when status is Discharged.')

        if status != 'Discharged' and admitted_out:
            self.add_error('admitted_out', 'Admitted out should only be set when the patient is discharged.')

        if room and status == 'Active':
            room_in_use = Admission.objects.filter(
                room=room,
                status='Active'
            ).exclude(pk=admission.pk if admission else None).exists()

            if room_in_use:
                self.add_error('room', 'This room is already occupied by another active admission.')

        if patient and status == 'Active':
            patient_already_active = Admission.objects.filter(
                patient=patient,
                status='Active'
            ).exclude(pk=admission.pk if admission else None).exists()

            if patient_already_active:
                self.add_error('patient', 'This patient already has an active admission.')

        if admission and status == 'Discharged':
            unpaid_bill_exists = Billing.objects.filter(
                admission=admission,
                payment_status__in=['Unpaid', 'Partially Paid']
            ).exists()

            if unpaid_bill_exists:
                self.add_error('status', 'Patient cannot be discharged because the admission bill is not fully paid.')

        return cleaned_data


class AdmissionSupplyUsageForm(forms.ModelForm):
    class Meta:
        model = AdmissionSupplyUsage
        fields = ['admission', 'supply', 'quantity_used', 'unit_cost', 'line_total', 'used_date']
        widgets = {
            'used_date': forms.DateInput(attrs={'type': 'date'}),
        }