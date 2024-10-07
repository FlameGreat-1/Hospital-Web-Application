from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Enrollment, WorkshopRegistration

@receiver(post_save, sender=Enrollment)
def send_enrollment_confirmation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'Enrollment Confirmation: {instance.course.title}',
            f'Dear {instance.user.get_full_name()},\n\nYou have successfully enrolled in the course "{instance.course.title}".\n\nBest regards,\nRalpha Hospital',
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )

@receiver(post_save, sender=WorkshopRegistration)
def send_workshop_registration_confirmation(sender, instance, created, **kwargs):
    if created:
        send_mail(
            f'Workshop Registration Confirmation: {instance.workshop.title}',
            f'Dear {instance.user.get_full_name()},\n\nYou have successfully registered for the workshop "{instance.workshop.title}".\n\nBest regards,\nRalpha Hospital',
            settings.DEFAULT_FROM_EMAIL,
            [instance.user.email],
            fail_silently=False,
        )
