from django.urls import path
from . import views

app_name = 'education_training'

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/enroll/', views.enroll_course, name='enroll_course'),
    path('workshops/', views.workshop_list, name='workshop_list'),
    path('workshops/<int:workshop_id>/', views.workshop_detail, name='workshop_detail'),
    path('workshops/<int:workshop_id>/register/', views.register_workshop, name='register_workshop'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('mark-attendance/<int:course_id>/', views.mark_attendance, name='mark_attendance'),
    path('generate-certificate/<int:course_id>/', views.generate_certificate, name='generate_certificate'),
    path('calendar-feed/', views.calendar_feed, name='calendar_feed'),
 
    


]
