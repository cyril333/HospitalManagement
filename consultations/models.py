from django.db import models
from patients.models import Patient
from accounts.models import User   # we'll define User next

class Consultation(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateField(auto_now_add=True)

class Prescription(models.Model):
    consultation = models.ForeignKey(Consultation, on_delete=models.CASCADE)
    # minimal for now