from django.db import models

class Patient(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=200)
    dateofbirth = models.DateField()
    age = models.IntegerField()
    status = models.CharField(max_length=100, default='Active')

    def __str__(self):
        return self.patient_name

    class Meta:
        db_table = 'patients'