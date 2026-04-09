from django.db import models
from patients.models import Patient
from departments.models import Room
from accounts.models import DoctorProfile
from inventory.models import Supplies

class Admission(models.Model):
    STATUS_CHOICES = [('Active', 'Active'), ('Discharged', 'Discharged'), ('Cancelled', 'Cancelled')]
    admission_id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    attending_doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True)
    admitted_in = models.DateTimeField()
    admitted_out = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"Admission #{self.admission_id} - {self.patient.patient_name}"

    class Meta:
        db_table = 'admission'

class AdmissionSupplyUsage(models.Model):
    usage_id = models.AutoField(primary_key=True)
    admission = models.ForeignKey(Admission, on_delete=models.CASCADE)
    supply = models.ForeignKey(Supplies, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)
    used_date = models.DateField()

    def __str__(self):
        return f"Usage #{self.usage_id}"

    class Meta:
        db_table = 'admission_supply_usage'