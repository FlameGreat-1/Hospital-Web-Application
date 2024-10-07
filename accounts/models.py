from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class BaseProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10)
    age = models.CharField(max_length=3)
    gender = models.CharField(max_length=10)
    otp = models.CharField(max_length=6)
    verify = models.CharField(max_length=1, default='0')
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Patient(BaseProfile):
    address = models.CharField(max_length=100)
    bloodgroup = models.CharField(max_length=10)
    casepaper = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.first_name} Patient'

class Doctor(BaseProfile):
    Department = models.CharField(max_length=20)
    attendance = models.CharField(max_length=10)
    status = models.CharField(max_length=15)
    salary = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.first_name} Doctor'

class StudentProfile(BaseProfile):
    institution = models.CharField(max_length=100, blank=True)
    field_of_study = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f'{self.user.first_name} Student'
