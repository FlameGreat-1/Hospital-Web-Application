from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from .models import HRPayment
from . import views
from django.template.response import TemplateResponse
from django.http import HttpResponse


class HRPaymentAdmin(admin.ModelAdmin):
    list_display = ('pmid', 'patient', 'outstanding', 'paid', 'total', 'date')
    list_filter = ('date',)
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    change_list_template = 'hr_change_list.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='admin_dashboard'),
            path('accounting/', self.admin_site.admin_view(self.accounting_view), name='admin_accounting'),
            path('payments/', self.admin_site.admin_view(self.payments_view), name='admin_payments'),
            path('showinvoice/', self.admin_site.admin_view(self.show_view), name='admin_showinvoice'),
            path('crtdoc/', self.admin_site.admin_view(self.crtdoc_view), name='admin_crtdoc'),
            path('updatedoc/', self.admin_site.admin_view(self.updatedoc_view), name='admin_updatedoc'),
            path('deletedoc/', self.admin_site.admin_view(self.deletedoc_view), name='admin_deletedoc'),
            path('send/', self.admin_site.admin_view(self.send_view), name='admin_send'),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        response = views.dashboard(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'dashboard.html', context)

    def accounting_view(self, request):
        response = views.accounting(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'accounting.html', context)

    def payments_view(self, request):
        response = views.payments(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'payments.html', context)

    def show_view(self, request):
        response = views.show(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'show.html', context)

    def crtdoc_view(self, request):
        response = views.crtdoc(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'crtdoc.html', context)

    def updatedoc_view(self, request):
        response = views.updatedoc(request)
        if isinstance(response, HttpResponse):
            return response
        context = response.context_data if hasattr(response, 'context_data') else {}
        return TemplateResponse(request, 'updatedoc.html', context)

    def deletedoc_view(self, request):
        return views.deletedoc(request)

    def send_view(self, request):
        return views.send(request)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_hr_buttons'] = True
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(HRPayment, HRPaymentAdmin)
