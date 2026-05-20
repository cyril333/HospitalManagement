from django.db import models
from django.core.exceptions import ValidationError
from patients.models import Patient
from departments.models import Room
from accounts.models import DoctorProfile
from inventory.models import Supplies


class Admission(models.Model):
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Discharged', 'Discharged'),
        ('Cancelled', 'Cancelled'),
    ]

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

    def clean(self):
        errors = {}

        if self.admitted_in and self.admitted_out and self.admitted_out <= self.admitted_in:
            errors['admitted_out'] = 'Admitted out must be later than admitted in.'

        if self.status == 'Discharged' and not self.admitted_out:
            errors['admitted_out'] = 'Discharge date and time is required when status is Discharged.'

        if self.status != 'Discharged' and self.admitted_out:
            errors['admitted_out'] = 'Admitted out should only be set when the patient is discharged.'

        if self.room_id and self.status == 'Active':
            room_in_use = Admission.objects.filter(
                room_id=self.room_id,
                status='Active'
            ).exclude(pk=self.pk).exists()

            if room_in_use:
                errors['room'] = 'This room is already occupied by another active admission.'

        if self.patient_id and self.status == 'Active':
            patient_already_active = Admission.objects.filter(
                patient_id=self.patient_id,
                status='Active'
            ).exclude(pk=self.pk).exists()

            if patient_already_active:
                errors['patient'] = 'This patient already has an active admission.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        previous_room_id = None
        if self.pk:
            previous_room_id = Admission.objects.filter(pk=self.pk).values_list('room_id', flat=True).first()

        super().save(*args, **kwargs)

        affected_room_ids = set()

        if previous_room_id:
            affected_room_ids.add(previous_room_id)

        if self.room_id:
            affected_room_ids.add(self.room_id)

        for room_id in affected_room_ids:
            has_active_admission = Admission.objects.filter(
                room_id=room_id,
                status='Active'
            ).exists()

            Room.objects.filter(pk=room_id).update(
                status='Occupied' if has_active_admission else 'Available'
            )


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