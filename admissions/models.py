from django.db import models
from patients.models import Patient

class Admission(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    admission_date = models.DateField(auto_now_add=True)
    # minimal fields

    def __str__(self):
        return f"Admission {self.id} - {self.patient}"