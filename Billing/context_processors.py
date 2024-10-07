# Billing/context_processors.py
from .models import Bill
from django.db.models import Sum

def billing_processor(request):
    if request.user.is_authenticated:
        total_due = Bill.objects.filter(
            patient=request.user, 
            status__in=['pending', 'partially_paid']
        ).aggregate(Sum('amount'))['amount__sum'] or 0
        return {'total_due': total_due}
    return {}
