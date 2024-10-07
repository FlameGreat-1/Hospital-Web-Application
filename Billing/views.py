import stripe
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Bill, Payment, Insurance
from .forms import PaymentForm, InsuranceForm

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def dashboard_view(request):
    bills = Bill.objects.filter(patient=request.user).order_by('-due_date')
    
    for bill in bills:
        bill.update_status()
    
    paginator = Paginator(bills, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    total_due = bills.filter(status__in=['pending', 'partially_paid', 'overdue']).aggregate(Sum('amount'))['amount__sum'] or 0
    
    insurance = Insurance.objects.filter(patient=request.user).first()
    
    recent_payments = Payment.objects.filter(bill__patient=request.user).order_by('-payment_date')[:5]
    
    context = {
        'page_obj': page_obj,
        'total_due': total_due,
        'insurance': insurance,
        'recent_payments': recent_payments,
    }
    return render(request, 'dashboard_1.html', context)

@login_required
def make_payment(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, patient=request.user)
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            try:
                intent = stripe.PaymentIntent.create(
                    amount=int(amount * 100),
                    currency='usd',
                    payment_method_types=['card'],
                    metadata={'bill_id': bill.id}
                )
                
                return JsonResponse({
                    'clientSecret': intent.client_secret
                })
            except stripe.error.StripeError as e:
                return JsonResponse({'error': str(e)}, status=400)
    else:
        form = PaymentForm(initial={'amount': bill.amount})
    
    context = {
        'form': form,
        'bill': bill,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY
    }
    return render(request, 'make_payment.html', context)

@csrf_exempt
@require_POST
def payment_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except stripe.error.SignatureVerificationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)
    
    return JsonResponse({'status': 'success'})

def handle_successful_payment(payment_intent):
    bill_id = payment_intent['metadata']['bill_id']
    amount = payment_intent['amount'] / 100
    
    bill = Bill.objects.get(id=bill_id)
    payment = Payment.objects.create(
        bill=bill,
        amount=amount,
        payment_method='credit_card',
        transaction_id=payment_intent['id'],
        status='completed'
    )
    
    if payment.amount >= bill.amount:
        bill.status = 'paid'
    else:
        bill.status = 'partially_paid'
    bill.save()

@login_required
def insurance_info(request):
    insurance = Insurance.objects.filter(patient=request.user).first()
    
    if request.method == 'POST':
        form = InsuranceForm(request.POST, instance=insurance)
        if form.is_valid():
            insurance = form.save(commit=False)
            insurance.patient = request.user
            insurance.save()
            messages.success(request, 'Insurance information updated successfully.')
            return redirect('Billing:insurance_info')
    else:
        form = InsuranceForm(instance=insurance)
    
    context = {
        'form': form,
        'insurance': insurance,
    }
    return render(request, 'billing/insurance_info.html', context)  

@login_required
def payment_history(request):
    payments = Payment.objects.filter(bill__patient=request.user).order_by('-payment_date')
    paginator = Paginator(payments, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'payment_history.html', context)

@login_required
def bill_detail(request, bill_id):
    bill = get_object_or_404(Bill, id=bill_id, patient=request.user)
    payments = bill.payments.all().order_by('-payment_date')
    
    context = {
        'bill': bill,
        'payments': payments,
    }
    return render(request, 'bill_detail.html', context)
