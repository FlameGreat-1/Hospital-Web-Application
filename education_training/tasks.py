from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Course, Workshop, Enrollment, WorkshopRegistration
from datetime import timedelta
from django.utils import timezone

@shared_task
def send_course_reminder():
    tomorrow = timezone.now().date() + timedelta(days=1)
    courses = Course.objects.filter(start_date=tomorrow)
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course)
        for enrollment in enrollments:
            send_mail(
                f'Reminder: {course.title} starts tomorrow',
                f'Dear {enrollment.user.get_full_name()},\n\nThis is a reminder that the course "{course.title}" starts tomorrow.\n\nBest regards,\nRalpha Hospital',
                settings.DEFAULT_FROM_EMAIL,
                [enrollment.user.email],
                fail_silently=False,
            )

@shared_task
def send_workshop_reminder():
    tomorrow = timezone.now().date() + timedelta(days=1)
    workshops = Workshop.objects.filter(date=tomorrow)
    for workshop in workshops:
        registrations = WorkshopRegistration.objects.filter(workshop=workshop)
        for registration in registrations:
            send_mail(
                f'Reminder: {workshop.title} is tomorrow',
                f'Dear {registration.user.get_full_name()},\n\nThis is a reminder that the workshop "{workshop.title}" is scheduled for tomorrow.\n\nBest regards,\nRalpha Hospital',
                settings.DEFAULT_FROM_EMAIL,
                [registration.user.email],
                fail_silently=False,
            )
