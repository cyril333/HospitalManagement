from django.contrib import admin
from .models import Department, Room

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name', 'status')
    search_fields = ('department_name',)

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_id', 'room_number', 'room_type', 'department', 'status', 'daily_rate')
    search_fields = ('room_number',)