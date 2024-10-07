# billing/tasks.py
from celery import shared_task
from django.utils import timezone
from .models import Bill

@shared_task
def send_bill_notifications():
    today = timezone.now().date()
    
    # Send overdue notifications
    overdue_bills = Bill.objects.filter(due_date__lt=today, status='pending')
    for bill in overdue_bills:
        bill.send_overdue_notification()
    
    # Send upcoming bill notifications (e.g., 3 days before due date)
    upcoming_bills = Bill.objects.filter(due_date=today + timezone.timedelta(days=3), status='pending')
    for bill in upcoming_bills:
        bill.send_upcoming_notification()
