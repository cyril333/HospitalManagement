from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone

# Foreign key references as strings to avoid circular imports
class Billing(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('PAID', 'Paid'),
        ('UNPAID', 'Unpaid'),
        ('PARTIALLY PAID', 'Partially Paid'),
    ]

    bill_id = models.AutoField(primary_key=True)  # implicit if not specified, but explicit is fine
    patient = models.ForeignKey('patients.Patient', on_delete=models.PROTECT, related_name='bills')
    admission = models.ForeignKey('admissions.Admission', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    consultation = models.ForeignKey('consultations.Consultation', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    prescription = models.ForeignKey('consultations.Prescription', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills')
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, editable=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    bill_date = models.DateField(default=timezone.now)

    def save(self, *args, **kwargs):
        # Auto-calculate total_amount
        self.total_amount = self.subtotal - self.discount
        # Optional: ensure total is not negative
        if self.total_amount < 0:
            self.total_amount = 0
        super().save(*args, **kwargs)

    def clean(self):
        # Ensure at least one chargeable entity is linked
        if not (self.admission or self.consultation or self.prescription):
            raise ValidationError('A bill must be linked to an admission, consultation, or prescription.')
        # If discount > subtotal, raise warning but we already cap total_amount >=0
        if self.discount > self.subtotal:
            raise ValidationError('Discount cannot exceed subtotal.')

    def __str__(self):
        return f"Bill {self.bill_id} - {self.patient} - {self.payment_status}"

    class Meta:
        ordering = ['-bill_date']