from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from .models import Patient, Doctor, StudentProfile
from django.contrib import messages
import random
from django.core.mail import send_mail
from prescriptions.models import Prescription
from HR.models import HRPayment

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']
        phone = request.POST['phone']
        typ = request.POST['type']
        if pass1 == pass2:
            if User.objects.filter(username=email).exists():
                messages.info(request, "Email Id already Exists!")
                return redirect('accounts:register')
            else:
                user = User.objects.create_user(first_name=fname, last_name=typ, username=email, password=pass1, email=email)
                o = str(random.randint(100000, 999999))
                if typ in ["Doctor", "Patient", "Nurse", "ICT", "Technician", "Contract worker", "Student"]:
                    if typ == "Doctor":
                        model = Doctor
                    elif typ == "Student":
                        model = StudentProfile
                    else:
                        model = Patient
                    pro = model(user=user, phone=phone, otp=o)
                    pro.save()
                    m = f'Hey {fname}!\nThank you for registering with the Ralpha Hospital and Maternity!\n\nYour OTP is: {o}'
                    send_mail('Registration Successful!', m, 'Ralpha Hospital and Maternity', [email], fail_silently=True)
                    messages.info(request, "Account Created Successfully")
                    return redirect('accounts:login')
        else:
            messages.info(request, "Passwords didn't match!")
            return redirect('accounts:register')
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('accounts:verify')
        else:
            messages.info(request, "Invalid Credentials!")
            return redirect('accounts:login')
    return render(request, 'login.html')

@login_required
def verify(request):
    user_type = request.user.last_name
    if user_type == "Doctor":
        pro = Doctor.objects.filter(user=request.user).first()
    elif user_type == "Student":
        pro = StudentProfile.objects.filter(user=request.user).first()
    else:
        pro = Patient.objects.filter(user=request.user).first()
    
    if request.method == 'POST':
        if 'submit1' in request.POST:
            o = request.POST['otp']
            if pro.otp == o:
                pro.verify = '1'
                pro.save()
                return redirect('accounts:profile')
            else:
                messages.info(request, "Invalid OTP!")
        elif 'resend' in request.POST:
            o = str(random.randint(100000, 999999))
            pro.otp = o
            pro.save()
            m = f'Hey {pro.user.first_name}!\nYour new OTP is: {o}'
            send_mail('OTP Resent', m, 'Ralpha Hospital and Maternity', [pro.user.email], fail_silently=True)
    return render(request, 'verify.html', {'user': request.user})

@login_required
def profile(request):
    user_type = request.user.last_name
    if user_type == "Doctor":
        pro = Doctor.objects.filter(user=request.user).first()
    elif user_type == "Student":
        pro = StudentProfile.objects.filter(user=request.user).first()
    else:
        pro = Patient.objects.filter(user=request.user).first()
    
    prescriptions = None
    invoices = None
    if user_type == "Patient":
        prescriptions = Prescription.objects.filter(patient=pro).order_by('-date')
        invoices = HRPayment.objects.filter(patient=pro).order_by('-date')
    
    if request.method == 'POST':
        if 'update' in request.POST:
            pro.phone = request.POST.get('phone', pro.phone)
            pro.gender = request.POST.get('gender', pro.gender)
            pro.age = request.POST.get('age', pro.age)
            if user_type == "Patient":
                pro.address = request.POST.get('address', pro.address)
                pro.bloodgroup = request.POST.get('bloodgroup', pro.bloodgroup)
                pro.casepaper = request.POST.get('casepaper', pro.casepaper)
            elif user_type == "Doctor":
                pro.Department = request.POST.get('dept', pro.Department)
                pro.attendance = request.POST.get('attn', pro.attendance)
                pro.salary = request.POST.get('salary', pro.salary)
                pro.status = request.POST.get('status', pro.status)
            elif user_type == "Student":
                pro.institution = request.POST.get('institution', pro.institution)
                pro.field_of_study = request.POST.get('field_of_study', pro.field_of_study)
            if 'image' in request.FILES:
                pro.image = request.FILES['image']
            pro.save()
            messages.success(request, "Profile updated successfully!")
        elif 'delete' in request.POST:
            user = request.user
            user.delete()
            messages.success(request, "Profile deleted successfully!")
            return redirect('accounts:login')
    
    context = {'pro': pro, 'prescriptions': prescriptions, 'invoices': invoices}
    return render(request, 'profile.html', context)

def logout(request):
    auth.logout(request)
    return redirect('accounts:login')

@login_required
def uprofile(request):
    user_type = request.user.last_name
    if user_type == "Patient":
        profile_model = Patient
    elif user_type == "Student":
        profile_model = StudentProfile
    elif user_type in ["Doctor", "Nurse", "ICT", "Technician", "Contract worker"]:
        profile_model = Doctor
    else:
        messages.error(request, "Invalid user type.")
        return redirect('accounts:profile')

    pro = profile_model.objects.filter(user=request.user).first()
    
    if not pro:
        messages.error(request, f"{user_type} profile not found.")
        return redirect('accounts:profile')

    if request.method == 'POST':
        pro.phone = request.POST.get('phone', pro.phone)
        pro.gender = request.POST.get('gender', pro.gender)
        pro.age = request.POST.get('age', pro.age)

        if user_type == "Patient":
            pro.address = request.POST.get('address', pro.address)
            pro.bloodgroup = request.POST.get('bloodgroup', pro.bloodgroup)
            pro.casepaper = request.POST.get('casepaper', pro.casepaper)
        elif user_type == "Student":
            pro.institution = request.POST.get('institution', pro.institution)
            pro.field_of_study = request.POST.get('field_of_study', pro.field_of_study)
        else:
            pro.Department = request.POST.get('dept', pro.Department)
            pro.attendance = request.POST.get('attn', pro.attendance)
            pro.salary = request.POST.get('salary', pro.salary)
            pro.status = request.POST.get('status', pro.status)
        
        if 'image' in request.FILES:
            pro.image = request.FILES['image']
        
        pro.save()
        messages.success(request, "Profile updated successfully.")
        return redirect('accounts:profile')

    context = {'pro': pro}
    return render(request, 'uprofile.html', context)

@login_required
def delete_confirmation(request):
    return render(request, 'delete_confirmation.html')

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user_type = user.last_name

        try:
            if user_type == "Patient":
                Patient.objects.get(user=user).delete()
            elif user_type == "Student":
                StudentProfile.objects.get(user=user).delete()
            elif user_type in ["Doctor", "Nurse", "ICT", "Technician", "Contract worker"]:
                Doctor.objects.get(user=user).delete()
            
            user.delete()
            auth.logout(request)
            messages.success(request, "Your profile has been successfully deleted.")
            return redirect('accounts:login')
        except Exception as e:
            messages.error(request, f"An error occurred while deleting your profile: {str(e)}")
            return redirect('accounts:profile')
    
    return redirect('accounts:delete_confirmation')
