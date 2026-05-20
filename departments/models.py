from django.db import models

class Department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='Active')

    def __str__(self):
        return self.department_name

    class Meta:
        db_table = 'department'

class Room(models.Model):
    STATUS_CHOICES = [('Available', 'Available'), ('Occupied', 'Occupied'), ('Maintenance', 'Maintenance')]
    room_id = models.AutoField(primary_key=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50, unique=True)
    room_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.room_number

    class Meta:
        db_table = 'rooms'