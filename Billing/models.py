from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings

class Bill(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('partially_paid', 'Partially Paid')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.patient.username} - ${self.amount}"

    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'pending'

    def update_status(self):
        if self.is_overdue():
            self.status = 'overdue'
            self.save()
            self.send_overdue_notification()

    def send_overdue_notification(self):
        subject = 'Your bill is overdue'
        message = f'Your bill of ${self.amount} was due on {self.due_date}. Please make a payment as soon as possible.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.patient.email])

    def send_upcoming_notification(self):
        subject = 'Upcoming bill reminder'
        message = f'You have a bill of ${self.amount} due on {self.due_date}. Please make a payment before the due date.'
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [self.patient.email])

class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], default='pending')

    def __str__(self):
        return f"Payment for Bill {self.bill.id} - ${self.amount}"

class Insurance(models.Model):
    patient = models.OneToOneField(User, on_delete=models.CASCADE)
    provider = models.CharField(max_length=100)
    policy_number = models.CharField(max_length=50)
    coverage_details = models.TextField()
    expiration_date = models.DateField()
    co_pay = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    deductible = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Insurance for {self.patient.username}"

    def is_valid(self):
        return self.expiration_date >= timezone.now().date()
