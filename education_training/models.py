from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    COURSE_TYPES = (
        ('MEDICAL', 'Medical'),
        ('NURSING', 'Nursing'),
        ('ADMIN', 'Administrative'),
        ('TECH', 'Technical'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    course_type = models.CharField(max_length=20, choices=COURSE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    capacity = models.PositiveIntegerField()
    instructor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='courses_taught')
    
    def __str__(self):
        return self.title

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'course')
    
    def __str__(self):
        return f"{self.user.username} - {self.course.title}"

class Workshop(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    duration = models.PositiveIntegerField(help_text="Duration in hours")
    location = models.CharField(max_length=200)
    capacity = models.PositiveIntegerField()
    
    def __str__(self):
        return self.title

class WorkshopRegistration(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'workshop')
    
    def __str__(self):
        return f"{self.user.username} - {self.workshop.title}"




class Attendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    is_present = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'course', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.date}"

class Certificate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    issue_date = models.DateField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/')

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Certificate"

