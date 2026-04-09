from django.db import models
from patients.models import Patient
from admissions.models import Admission
from consultations.models import Consultation, Prescription

class Billing(models.Model):
    PAYMENT_CHOICES = [('Paid', 'Paid'), ('Unpaid', 'Unpaid'), ('Partially Paid', 'Partially Paid')]
    bill_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission = models.ForeignKey(Admission, null=True, blank=True, on_delete=models.SET_NULL)
    consultation = models.ForeignKey(Consultation, null=True, blank=True, on_delete=models.SET_NULL)
    prescription = models.ForeignKey(Prescription, null=True, blank=True, on_delete=models.SET_NULL)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='Unpaid')
    bill_date = models.DateField()

    def __str__(self):
        return f"Bill #{self.bill_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'billing'