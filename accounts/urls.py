from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('verify/', views.verify, name='verify'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout, name='logout'),
    path('update-profile/', views.uprofile, name='update_profile'),
    path('delete-profile/', views.delete_profile, name='delete_profile'),
    path('delete-confirmation/', views.delete_confirmation, name='delete_confirmation'),
    # New password reset URLs
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
