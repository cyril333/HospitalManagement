from django.db import models
from patients.models import Patient
from accounts.models import DoctorProfile
from inventory.models import InventoryMedicine

class Consultation(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    consultation_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    consultation_date = models.DateField()
    consultation_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Consultation #{self.consultation_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'consultation'

class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    record_date = models.DateField()

    def __str__(self):
        return f"Record #{self.record_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'medical_records'

class Prescription(models.Model):
    prescription_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    prescription_date = models.DateField()
    total_items = models.IntegerField(default=0)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Prescription #{self.prescription_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'prescription'

class PrescriptionItem(models.Model):
    prescription_item_id = models.AutoField(primary_key=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)
    medicine = models.ForeignKey(InventoryMedicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    dosage = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Item #{self.prescription_item_id}"

    class Meta:
        db_table = 'prescription_item'