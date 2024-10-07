from django.contrib import admin
from accounts.models import Patient,Doctor,StudentProfile

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(StudentProfile)
