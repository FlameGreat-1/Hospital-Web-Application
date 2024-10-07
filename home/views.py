from django.shortcuts import render
from django.views.generic import TemplateView
from django.templatetags.static import static
from Departments.models import Doctors 
from django.db import models
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .forms import ContactForm
from News.models import News  
from Billing.models import Bill
from django.db.models import Sum
from education_training.models import Workshop, Course
from django.utils import timezone


# View for Home Page
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ralpha Hospital and Maternity'
        context['services'] = [
            {
                'title': 'Our Services',
                'description': 'Learn about our medical services provided by our team of experts.',
                'link': 'home:our_services',
                'image': 'services.jpg'
            },
            {
                'title': 'Appointments',
                'description': 'Learn how we strive to keep you comfortable during your stay with us.',
                'link': 'appointments:setapt',
                'image': 'Appointments.jpg'
            },
            {
                'title': 'Location',
                'description': '87 Afikpo Road, Abakaliki, Ebonyi state.',
                'link': 'home:location',
                'image': 'Location.png'
            }
        ]
        context['news_items'] = News.objects.all().order_by('-publication_date')[:3]  # Get the 3 most recent news items
        
        if self.request.user.is_authenticated:
            total_due = Bill.objects.filter(
                patient=self.request.user, 
                status__in=['pending', 'partially_paid']
            ).aggregate(Sum('amount'))['amount__sum'] or 0
            context['total_due'] = total_due
        
        # Add Education and Training data
        context['upcoming_workshops'] = Workshop.objects.filter(date__gte=timezone.now()).order_by('date')[:3]
        context['latest_courses'] = Course.objects.order_by('-start_date')[:3]
        
        return context


# View for Find a Doctor page
class FindDoctorView(TemplateView):
    template_name = 'find_doctor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Find A Doctor'
        context['description'] = (
            'We have experts specializing in a wide range of medical practices. '
            'Our experts at The Ralpha Hospital and Maternity are here to provide you with the care you need.'
        )
        
        # Get the search term from the query parameters
        search_term = self.request.GET.get('query', '')
        if search_term:
            # Filter doctors by name or specialty
            context['doctors'] = Doctors.objects.filter(
                models.Q(first_name__icontains=search_term) | 
                models.Q(last_name__icontains=search_term) | 
                models.Q(specialty__icontains=search_term)
            )
        else:
            context['doctors'] = Doctors.objects.none()
        
        return context


class OurServicesView(TemplateView):
    template_name = 'our_services.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Our Services'
        context['services'] = [
            {'title': 'Maternity Care', 'description': 'Comprehensive maternity care services from prenatal to postpartum.', 'image': static('images/maternity.jpg')},
            {'title': 'General Surgery', 'description': 'World-class surgical care for a variety of conditions.', 'image': static('images/surgery.jpg')},
            {'title': 'Pediatrics', 'description': 'Specialized care for children by expert pediatricians.', 'image': static('images/pediatrics.jpg')},
            {'title': 'Emergency Services', 'description': '24/7 emergency care for critical conditions.', 'image': static('images/emergency.jpg')},
            {'title': 'Radiology', 'description': 'Advanced imaging services including X-ray, MRI, and ultrasound.', 'image': static('images/radiology.jpg')}
        ]
        return context

# View for Location page
class LocationView(TemplateView):
    template_name = 'location.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Location'
        context['address'] = '87 Afikpo Road, Abakaliki 480108, Ebonyi'
        return context


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                f'Contact Form Submission: {subject}',
                f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}',
                email,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Your message has been sent. Thank you!')
            return redirect('contact_us')
    else:
        form = ContactForm()
    
    return render(request, 'contact_us.html', {'form': form})


class AboutUsView(TemplateView):
    template_name = 'about_us.html'
