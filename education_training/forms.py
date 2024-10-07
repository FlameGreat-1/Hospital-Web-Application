from django import forms
from .models import Course, Workshop

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'course_type', 'start_date', 'end_date', 'capacity', 'instructor']

class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = ['title', 'description', 'date', 'duration', 'location', 'capacity']
