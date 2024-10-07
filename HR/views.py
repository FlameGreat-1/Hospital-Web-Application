from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Doctor, Patient
from .models import HRPayment
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User






# Create your views here.
@login_required
def dashboard(request):
    p = Doctor.objects.all()
    ad = len(Doctor.objects.filter(status="ACTIVE").all())
    tot = len(p)
    k = len(Patient.objects.all())
    c = {'p': p, 'tot': tot, 'k': k, 'ad': ad}             
    return render(request, "dashboard.html", c)

@login_required
def deletedoc(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        px = Doctor.objects.filter(did=pid).first()
        if px:
            us = User.objects.filter(username=px.user.username).first()
            if us:
                us.delete()        
    return redirect("dashboard")

@login_required
def crtdoc(request):
    if request.method == 'POST':
        fname = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        status = request.POST.get('status')
        salary = request.POST.get('salary')
        dept = request.POST.get('dept')
        attn = request.POST.get('attn')
        if User.objects.filter(username=email).exists():
            messages.info(request, "Doctor already exists!!")
            return redirect('crtdoc')
        else:
            user = User.objects.create_user(first_name=fname, last_name='Doctor', username=email, email=email)
            pro = Doctor(user=user, phone=phone, gender=gender, age=age, status=status, salary=salary, attendance=attn, Department=dept)
            pro.save()
            return redirect('dashboard')
    return render(request, 'crtdoc.html')

@login_required
def updatedoc(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        pro = Doctor.objects.filter(did=pid).first()
        return render(request, 'uprofile.html', {'pro': pro})
    else:
        # Handle GET request
        doctors = Doctor.objects.all()
        return render(request, 'updatedoc.html', {'doctors': doctors})

@login_required
def accounting(request):
    p = Patient.objects.all()
    if request.method == 'POST':
        pat = request.POST.get('pat')
        us = User.objects.filter(first_name=pat).first()
        if us:
            pe = Patient.objects.filter(user=us).first()
            if pe:
                paid = int(request.POST.get('paid', 0))
                out = int(request.POST.get('out', 0))
                tot = paid + out
                tax = 0.05 * tot
                tot = tot + tax
                pay = HRPayment(patient=pe, paid=paid, outstanding=out, total=tot)
                pay.save()
    payt = HRPayment.objects.all()
    return render(request, 'accounting.html', {'p': p, 'payt': payt})

@login_required
def send(request):
    if request.method == 'POST':
        pmid = request.POST.get('pid')
        inv = HRPayment.objects.filter(pmid=pmid).first()
        if inv:
            m = f'Hey {inv.patient}!\n\nYour outstanding billing amount is : {inv.outstanding}$\n\nYour Total Billing amount is : {inv.total}$\n\nYour Paid Billing amount is : {inv.paid}$'
            send_mail('Payment Reminder!', m, 'Hospital Management System', [inv.patient.user.username], fail_silently=True)
    return redirect('accounting')

@login_required
def payments(request):
    pat = Patient.objects.filter(user=request.user).first()
    payt = HRPayment.objects.filter(patient=pat).all()
    return render(request, "payments.html", {'payt': payt})

@login_required
def show(request):
    inv = None  # Initialize `inv` to handle GET requests and avoid UnboundLocalError
    
    if request.method == 'POST':
        pmid = request.POST.get('pid')
        inv = HRPayment.objects.filter(pmid=pmid).first()
    
    return render(request, 'show.html', {'inv': inv})









