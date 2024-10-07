# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Department, Staff, Expense, Payroll, Message
from django.db.models import Sum
from .models import Payroll 
from .models import Message
from .models import Expense
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import Doctor, Patient
from django.core.mail import send_mail
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    departments = Department.objects.all()
    staff_count = Staff.objects.count()
    total_expenses = Expense.objects.filter(Approved=True).aggregate(Sum('Amount'))['Amount__sum'] or 0
    total_income = Department.objects.aggregate(Sum('Income_generated'))['Income_generated__sum'] or 0
    doctors = Doctor.objects.all()
    active_doctors = Doctor.objects.filter(status="ACTIVE").count()
    patients = Patient.objects.all()
    context = {
        'departments': departments,
        'staff_count': staff_count,
        'total_expenses': total_expenses,
        'total_income': total_income,
        'doctors': doctors,
        'active_doctors': active_doctors,
        'patients': patients,
    }
    return render(request, 'dashboard.html', context)

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'department_list.html', {'departments': departments})

@login_required
def staff_list(request):
    staff = Staff.objects.all()
    return render(request, 'staff_list.html', {'staff': staff})

@login_required
def expense_list(request):
    expenses = Expense.objects.all()
    return render(request, 'expense_list.html', {'expenses': expenses})

@login_required
def payroll_list(request):
    payrolls = Payroll.objects.all()
    return render(request, 'payroll_list.html', {'payrolls': payrolls})

@login_required
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'message_list.html', {'messages': messages})

@login_required
def approve_expense(request, expense_id):
    expense = get_object_or_404(Expense, id=expense_id)
    if request.method == 'POST':
        expense.Approved = True
        expense.Approved_by = request.user
        expense.save()
        messages.success(request, 'Expense approved successfully.')
    return redirect('Dashboard:expense_list')  # Updated to use the correct URL name

################################.........HR MANAGEMENT..............############################
