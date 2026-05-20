from django.contrib import admin
from .models import UserProfile, AdminProfile, DoctorProfile, NurseProfile

admin.site.register(UserProfile)
admin.site.register(AdminProfile)
admin.site.register(DoctorProfile)
admin.site.register(NurseProfile)