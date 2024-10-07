
from django.urls import path
from django.utils.translation import gettext_lazy as _
from . import views
from .views import HomeView, FindDoctorView, OurServicesView, LocationView
from .views import HomeView, AboutUsView  

app_name = 'home'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('find-doctor/', FindDoctorView.as_view(), name='find_doctor'),  
    path('our-services/', OurServicesView.as_view(), name='our_services'),
    path('location/', LocationView.as_view(), name='location'),
    path('contact/', views.contact_us, name='contact_us'),
    path('about/', AboutUsView.as_view(), name='about_us'),
     
     
]
