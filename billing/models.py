# billing/models.py

from decimal import Decimal
from django.db import models
from django.db.models import Sum
from django.core.exceptions import ValidationError
from django.utils import timezone
from patients.models import Patient
from admissions.models import Admission
from consultations.models import Consultation, Prescription, PrescriptionItem


class Billing(models.Model):
    PAYMENT_CHOICES = [('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Partially Paid', 'Partially Paid')]

    bill_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.SET_NULL)
    consultation = models.ForeignKey(Consultation, null=True, blank=True, on_delete=models.SET_NULL)
    prescription = models.ForeignKey(Prescription, null=True, blank=True, on_delete=models.SET_NULL)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Unpaid')
    bill_date = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"Bill #{self.bill_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'billing'

    def get_billing_end_datetime(self):
        if not self.admission or not self.admission.admitted_in:
            return None

        if self.admission.admitted_out:
            return self.admission.admitted_out

        if self.admission.status == 'Active':
            return timezone.now()

        return None

    def get_admission_days(self):
        if not self.admission or not self.admission.admitted_in:
            return 0

        admitted_in = self.admission.admitted_in
        billing_end = self.get_billing_end_datetime()

        if not billing_end:
            return 0

        if billing_end <= admitted_in:
            return 1

        duration = billing_end - admitted_in
        days = duration.days
        if duration.seconds > 0:
            days += 1

        return max(days, 1)

    def get_doctor_charge(self):
        if not self.admission or not self.admission.attending_doctor:
            return Decimal('0.00')

        daily_rate = self.admission.attending_doctor.daily_rate or Decimal('0.00')
        days = self.get_admission_days()
        return Decimal(days) * daily_rate

    def get_room_charge(self):
        if not self.admission or not self.admission.room:
            return Decimal('0.00')

        daily_rate = self.admission.room.daily_rate or Decimal('0.00')
        days = self.get_admission_days()
        return Decimal(days) * daily_rate

    def get_admission_charge(self):
        return self.get_doctor_charge() + self.get_room_charge()

    def get_prescription_charge(self):
        if not self.prescription:
            return Decimal('0.00')

        total = PrescriptionItem.objects.filter(
            prescription=self.prescription
        ).aggregate(total=Sum('unit_price'))['total']

        return total or Decimal('0.00')

    def calculate_subtotal(self):
        admission_charge = self.get_admission_charge()
        prescription_charge = self.get_prescription_charge()
        return admission_charge + prescription_charge

    def calculate_total_amount(self):
        subtotal = self.calculate_subtotal()
        discount_percent = self.discount or Decimal('0.00')
        discount_amount = subtotal * (discount_percent / Decimal('100'))
        total = subtotal - discount_amount
        return total if total >= 0 else Decimal('0.00')

    def clean(self):
        errors = {}

        if self.discount is not None and self.discount < 0:
            errors['discount'] = 'Discount percentage cannot be negative.'

        if self.discount is not None and self.discount > 100:
            errors['discount'] = 'Discount percentage cannot be greater than 100.'

        if self.admission and self.patient_id != self.admission.patient_id:
            errors['admission'] = 'Selected admission does not belong to the selected patient.'

        if self.consultation and self.patient_id != self.consultation.patient_id:
            errors['consultation'] = 'Selected consultation does not belong to the selected patient.'

        if self.prescription and self.patient_id != self.prescription.patient_id:
            errors['prescription'] = 'Selected prescription does not belong to the selected patient.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.subtotal = self.calculate_subtotal()
        self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)