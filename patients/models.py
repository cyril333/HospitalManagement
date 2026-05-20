from datetime import date
from django.db import models


class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=200)
    dateofbirth = models.DateField()
    age = models.IntegerField(default=0)
    status = models.CharField(max_length=100, default='Active')

    def __str__(self):
        return self.patient_name

    class Meta:
        db_table = 'patients'

    def calculate_age(self):
        today = date.today()
        age = today.year - self.dateofbirth.year
        if (today.month, today.day) < (self.dateofbirth.month, self.dateofbirth.day):
            age -= 1
        return age

    def save(self, *args, **kwargs):
        if self.dateofbirth:
            self.age = self.calculate_age()
        super().save(*args, **kwargs)