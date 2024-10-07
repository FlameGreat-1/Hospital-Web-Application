from django.db import models
from accounts.models import Patient, Doctor
from django.core.mail import send_mail
from django.conf import settings

class Appointment(models.Model):
    aid = models.AutoField(primary_key=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default="Pending")
    date = models.CharField(max_length=20)
    time = models.CharField(max_length=20)
    is_approved = models.BooleanField(default=False)  # New field for approval status
    
    def __str__(self):
        return f"Appointment {self.aid} - {self.patient.user.first_name} with {self.doctor.user.first_name}"

    def send_approval_notification(self):
        # Email notification
        subject = "Your Appointment has been Approved"
        message = f"Dear {self.patient.user.first_name},\n\nYour appointment with Dr. {self.doctor.user.first_name} has been approved.\nDate: {self.date}\nTime: {self.time}\n"
        recipient_email = self.patient.user.email
        send_mail(subject, message, settings.EMAIL_HOST_USER, [recipient_email])

        # SMS notification can be added here with an external service
