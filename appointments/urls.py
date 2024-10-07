from django.urls import path
from . import views
from accounts.views import login



app_name = 'appointments'

urlpatterns = [
    path('login/', login, name='login'),  # Use the login from the accounts app
    path('', views.appointments, name='appointments'),
    path('reception/', views.reception, name='reception'),
    path('setapt/', views.setapt, name='setapt'),
    path('createpat/', views.createpat, name='createpat'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('updatepat/', views.updatepat, name='updatepat'),
    path('deletepat/', views.deletepat, name='deletepat'),

]
