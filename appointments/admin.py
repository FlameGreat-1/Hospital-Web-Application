from django.contrib import admin
from .models import Appointment, Patient
from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Appointment
from accounts.models import Patient
from django.template.response import TemplateResponse





class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'is_approved')
    actions = ['approve_appointments']
    list_filter = ('status', 'date')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name', 'status')
    change_list_template = 'appointment_change_list.html'

    def approve_appointments(self, request, queryset):
        for appointment in queryset:
            appointment.is_approved = True
            appointment.save()
            appointment.send_approval_notification()
        self.message_user(request, "Selected appointments have been approved and notifications sent.")

    approve_appointments.short_description = "Approve selected appointments"



    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('reception/', self.admin_site.admin_view(self.reception_view), name='appointment_reception'),
        ]
        return custom_urls + urls

    def reception_view(self, request):
        ap = Appointment.objects.all()
        p = Patient.objects.all()
        tot = ap.count()
        pending = ap.filter(status="Pending").count()
        com = ap.filter(status="Completed").count()
        context = {
            'ap': ap,
            'p': p,
            'tot': tot,
            'pend': pending,
            'com': com,
            'title': 'Reception',
            'opts': self.model._meta,
        }
        return TemplateResponse(request, 'reception.html', context)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_reception_button'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Appointment, AppointmentAdmin)
