from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Course, Enrollment, Workshop, WorkshopRegistration, Attendance, Certificate
from django.db import models
from django.contrib.auth.models import User


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_type', 'start_date', 'end_date', 'capacity', 'instructor')
    list_filter = ('course_type', 'start_date')
    search_fields = ('title', 'description', 'instructor__username')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrollment_date')
    list_filter = ('course', 'enrollment_date')
    search_fields = ('user__username', 'course__title')

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'duration', 'location', 'capacity')
    list_filter = ('date',)
    search_fields = ('title', 'description', 'location')

@admin.register(WorkshopRegistration)
class WorkshopRegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'workshop', 'registration_date')
    list_filter = ('workshop', 'registration_date')
    search_fields = ('user__username', 'workshop__title')



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'date', 'is_present')
    list_filter = ('course', 'date', 'is_present')
    search_fields = ('user__username', 'course__title')



@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'issue_date')
    list_filter = ('course', 'issue_date')
    search_fields = ('user__username', 'course__title')


