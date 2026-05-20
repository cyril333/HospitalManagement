from django.db import models

class Patient(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Discharged', 'Discharged'),
        ('Critical', 'Critical'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dateofbirth = models.DateField()
    age = models.IntegerField(editable=False, default=0)
    blood_type = models.CharField(max_length=5, choices=BLOOD_TYPE_CHOICES, blank=True)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_number = models.CharField(max_length=20)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Active')

    def save(self, *args, **kwargs):
        # Auto-calculate age from date of birth
        from datetime import date
        today = date.today()
        self.age = today.year - self.dateofbirth.year - (
            (today.month, today.day) < (self.dateofbirth.month, self.dateofbirth.day)
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.patient_name

    class Meta:
        db_table = 'patients'