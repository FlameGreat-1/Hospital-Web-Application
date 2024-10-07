from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Prescription
from accounts.models import Patient
from django.template.response import TemplateResponse

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prid', 'patient', 'doctor', 'disease', 'date')
    list_filter = ('doctor', 'disease', 'date')
    search_fields = ('patient__user__first_name', 'doctor__user__first_name', 'disease')
    change_list_template = 'prescription_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('showpres/', self.admin_site.admin_view(self.showpres_view), name='admin_showpres'),
            path('showmedhis/', self.admin_site.admin_view(self.showmedhis_view), name='admin_showmedhis'),
        ]
        return custom_urls + urls

    def showpres_view(self, request):
        pre = Prescription.objects.all()
        context = {'pre': pre, 'title': 'Show Prescriptions'}
        return TemplateResponse(request, 'showpres.html', context)

    def showmedhis_view(self, request):
        doc = Patient.objects.filter(user=request.user).first()
        pre = Prescription.objects.filter(patient=doc).all()
        context = {'pre': pre, 'title': 'Medical History'}
        return TemplateResponse(request, 'showmedhis.html', context)

admin.site.register(Prescription, PrescriptionAdmin)
