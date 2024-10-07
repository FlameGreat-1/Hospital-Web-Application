from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import User
from .models import Bill, Payment, Insurance
from django.contrib import messages
import datetime

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('patient', 'amount', 'due_date', 'status')
    list_filter = ('status', 'due_date')
    search_fields = ('patient__username', 'patient__email', 'description')
    date_hierarchy = 'due_date'
    
    actions = ['generate_monthly_bills']

    def generate_monthly_bills(self, request, queryset):
        users = User.objects.all()
        bills_created = 0
        for user in users:
            Bill.objects.create(
                patient=user,
                amount=100.00,  # You can adjust this or make it dynamic
                due_date=datetime.date.today() + datetime.timedelta(days=30),
                description="Monthly Service Fee",
                status='pending'
            )
            bills_created += 1
        self.message_user(request, f"{bills_created} bills were created successfully.", messages.SUCCESS)
    generate_monthly_bills.short_description = "Generate monthly bills for all users"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'amount', 'payment_date', 'payment_method', 'status')
    list_filter = ('status', 'payment_date')
    search_fields = ('bill__patient__username', 'transaction_id')
    date_hierarchy = 'payment_date'

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('patient', 'provider', 'policy_number', 'expiration_date')
    list_filter = ('provider', 'expiration_date')
    search_fields = ('patient__username', 'provider', 'policy_number')
    date_hierarchy = 'expiration_date'
