from django.db import models
from django.utils import timezone
from accounts.models import Patient
from django.contrib.auth.models import User


# Payment Models
class HRPayment(models.Model):
    pmid = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='hr_payments')
    outstanding = models.IntegerField(default=0)
    paid = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f'Payment ID: {self.pmid} - Patient: {self.patient}'




class HRDashboard(models.Model):
    class Meta:
        verbose_name_plural = 'HR Dashboard'
        app_label = 'hr'

