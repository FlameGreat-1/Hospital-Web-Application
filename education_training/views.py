from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Course, Enrollment, Workshop, WorkshopRegistration, Attendance, Certificate
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from django.utils import timezone
from icalendar import Calendar, Event
from datetime import datetime, timedelta
import pytz





def course_list(request):
    courses = Course.objects.all().order_by('start_date')
    paginator = Paginator(courses, 10)  # Show 10 courses per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'education_training/course_list.html', {'page_obj': page_obj})



def course_detail(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    is_enrolled = request.user.is_authenticated and Enrollment.objects.filter(user=request.user, course=course).exists()
    return render(request, 'education_training/course_detail.html', {'course': course, 'is_enrolled': is_enrolled})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if Enrollment.objects.filter(user=request.user, course=course).exists():
        messages.warning(request, "You are already enrolled in this course.")
    elif Enrollment.objects.filter(course=course).count() >= course.capacity:
        messages.error(request, "This course is already full.")
    else:
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f"You have successfully enrolled in {course.title}.")
    return redirect('education_training:course_detail', course_id=course.id)

def workshop_list(request):
    workshops = Workshop.objects.all().order_by('date')
    paginator = Paginator(workshops, 10)  # Show 10 workshops per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'education_training/workshop_list.html', {'page_obj': page_obj})

def workshop_detail(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    is_registered = request.user.is_authenticated and WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists()
    return render(request, 'education_training/workshop_detail.html', {'workshop': workshop, 'is_registered': is_registered})

@login_required
def register_workshop(request, workshop_id):
    workshop = get_object_or_404(Workshop, pk=workshop_id)
    if WorkshopRegistration.objects.filter(user=request.user, workshop=workshop).exists():
        messages.warning(request, "You are already registered for this workshop.")
    elif WorkshopRegistration.objects.filter(workshop=workshop).count() >= workshop.capacity:
        messages.error(request, "This workshop is already full.")
    else:
        WorkshopRegistration.objects.create(user=request.user, workshop=workshop)
        messages.success(request, f"You have successfully registered for {workshop.title}.")
    return redirect('workshop_detail', workshop_id=workshop.id)




@login_required
def user_dashboard(request):
    user_enrollments = Enrollment.objects.filter(user=request.user).select_related('course')
    user_workshops = WorkshopRegistration.objects.filter(user=request.user).select_related('workshop')
    user_certificates = Certificate.objects.filter(user=request.user).select_related('course')
    
    context = {
        'enrollments': user_enrollments,
        'workshops': user_workshops,
        'certificates': user_certificates,
    }
    return render(request, 'education_training/user_dashboard.html', context)

@login_required
def mark_attendance(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.method == 'POST':
        date = request.POST.get('date')
        is_present = request.POST.get('is_present') == 'on'
        Attendance.objects.update_or_create(
            user=request.user,
            course=course,
            date=date,
            defaults={'is_present': is_present}
        )
        messages.success(request, "Attendance marked successfully.")
    return redirect('course_detail', course_id=course.id)

@login_required
def generate_certificate(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
    
    # Check if the user has completed the course (e.g., attended at least 80% of classes)
    total_days = (course.end_date - course.start_date).days + 1
    attended_days = Attendance.objects.filter(user=request.user, course=course, is_present=True).count()
    attendance_percentage = (attended_days / total_days) * 100
    
    if attendance_percentage < 80:
        messages.error(request, "You need to attend at least 80% of the classes to receive a certificate.")
        return redirect('course_detail', course_id=course.id)
    
    # Generate PDF certificate
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{course.title}_certificate.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.setFont("Helvetica-Bold", 24)
    p.drawCentredString(4.25*inch, 8*inch, "Certificate of Completion")
    p.setFont("Helvetica", 16)
    p.drawCentredString(4.25*inch, 7*inch, f"This is to certify that")
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(4.25*inch, 6.5*inch, f"{request.user.get_full_name()}")
    p.setFont("Helvetica", 16)
    p.drawCentredString(4.25*inch, 6*inch, f"has successfully completed the course")
    p.setFont("Helvetica-Bold", 18)
    p.drawCentredString(4.25*inch, 5.5*inch, f"{course.title}")
    p.setFont("Helvetica", 16)
    p.drawCentredString(4.25*inch, 5*inch, f"on {timezone.now().strftime('%B %d, %Y')}")
    p.setFont("Helvetica-Bold", 14)
    p.drawCentredString(4.25*inch, 2*inch, "Ralpha Hospital and Maternity")
    p.showPage()
    p.save()
    
    # Save the certificate in the database
    certificate, created = Certificate.objects.get_or_create(
        user=request.user,
        course=course,
        defaults={'certificate_file': f"{course.title}_certificate.pdf"}
    )
    
    return response

def calendar_feed(request):
    cal = Calendar()
    cal.add('prodid', '-//Ralpha Hospital Education Calendar//example.com//')
    cal.add('version', '2.0')

    courses = Course.objects.all()
    workshops = Workshop.objects.all()

    for course in courses:
        event = Event()
        event.add('summary', course.title)
        event.add('dtstart', course.start_date)
        event.add('dtend', course.end_date + timedelta(days=1))  # Add one day to include the end date
        event.add('description', course.description)
        cal.add_component(event)

    for workshop in workshops:
        event = Event()
        event.add('summary', workshop.title)
        event.add('dtstart', workshop.date)
        event.add('dtend', workshop.date + timedelta(hours=workshop.duration))
        event.add('description', workshop.description)
        cal.add_component(event)

    response = HttpResponse(cal.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename=education_calendar.ics'
    return response
