from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment
from accounts.models import Doctor, Patient
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from accounts.views import login

@login_required
def appointments(request):
    if request.user.last_name == "Patient":
        pro = Patient.objects.filter(user=request.user).first()
        ap = Appointment.objects.filter(patient=pro).all()
    elif request.user.last_name == "Doctor":
        pro = Doctor.objects.filter(user=request.user).first()
        ap = Appointment.objects.filter(doctor=pro).all()
    else:
        ap = []

    return render(request, 'appointments.html', {'ap': ap})

@login_required
def setapt(request):
    d = Doctor.objects.all()
    p = Patient.objects.all()
    da = list(range(1, 32))
    y = list(range(2020, 2031))
    h = list(range(1, 13))
    m = ['00', '15', '30', '45']

    if request.method == 'POST':
        hours = request.POST['hours']
        min = request.POST['min']
        am = request.POST['am']
        time = f"{hours} : {min} {am}"
        doc = request.POST['doc']
        pat = request.POST['pat']
        sta = request.POST['status']
        dat = request.POST['d']
        month = request.POST['m']
        year = request.POST['y']
        date = f"{dat}-{month}-{year}"

        user1 = User.objects.filter(first_name=pat).first()
        user2 = User.objects.filter(first_name=doc).first()

        if not user1 or not user2:
            messages.error(request, "Doctor or Patient not found")
            return redirect('appointments:setapt')

        pa = Patient.objects.filter(user=user1).first()
        do = Doctor.objects.filter(user=user2).first()

        if not pa or not do:
            messages.error(request, "Doctor or Patient not found")
            return redirect('appointments:setapt')

        # Create and save the appointment
        a = Appointment.objects.create(
            patient=pa,
            doctor=do,
            time=time,
            date=date,
            status=sta
        )
        a.save()

        messages.success(request, "Appointment created successfully!")
        return redirect('appointments:createpat')

    return render(request, 'setapt.html', {'d': d, 'p': p, 'm': m, 'da': da, 'y': y, 'h': h})

# Reception access for admin
@login_required
def reception(request):
    ap = Appointment.objects.all()
    p = Patient.objects.all()
    tot = len(ap)
    pending = len(Appointment.objects.filter(status="Pending").all())
    com = len(Appointment.objects.filter(status="Completed").all())
    return render(request, 'reception.html', {'ap': ap, 'p': p, 'tot': tot, 'pend': pending, 'com': com})





@login_required
def createpat(request):
    if request.method == 'POST':        
        try:
            _, file = request.FILES.popitem()
            file = file[0]
            image = file
        except:
            image = None

        fname = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        gender = request.POST['gender']
        age = request.POST['age']
        add = request.POST['address']
        bg = request.POST['bloodgroup']
        casepaper = request.POST['casepaper']

        if User.objects.filter(username=email).exists():
            messages.info(request, "Email Id already Exists!")
            return redirect('appointments:createpat')
        else:
            user = User.objects.create_user(first_name=fname, last_name='Patient', username=email, email=email)
            pro = Patient(user=user, phone=phone, gender=gender, age=age, address=add, bloodgroup=bg, casepaper=casepaper, image=image)
            pro.save()
            
            # Add success message
            messages.success(request, "Thank you! Your appointment has been sent and you will be notified if approved")
            return redirect('appointments:confirmation')

    return render(request, 'createpat.html')



def confirmation(request):
    return render(request, 'confirmation.html')



@login_required
def updatepat(request):
    if request.method == 'POST':
        pid = request.POST.get('pid')
        pro = Patient.objects.filter(pid=pid).first()

        if not pro:
            messages.error(request, "Patient not found.")
            return redirect('appointments:reception')  # Redirect if not found or handle it

        return render(request, 'uprofile.html', {'pro': pro})

    else:
        return render(request, 'updatepat.html')  # Display the update patient page or form
    

@login_required
def deletepat(request):
    if request.method == 'POST':
        pid = request.POST['pid']
        px = Patient.objects.filter(pid=pid).first()
        us = User.objects.filter(username=px.user.username).first()
        us.delete()
        return redirect("appointments:reception") 
    ap = Appointment.objects.all()
    p = Patient.objects.all()
    c = {'ap': ap, 'p': p}
    return render(request, 'reception.html', c)



















from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from .models import Appointment
from accounts.models import Doctor,Patient
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse


