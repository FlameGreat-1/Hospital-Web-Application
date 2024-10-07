from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from accounts import views
from django.contrib.auth import views as auth_views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in auth views
    path("departments/", include("Departments.urls")),
    path('appointments/', include('appointments.urls', namespace='appointments')),
    path('', include('home.urls')),
    path('HR/', include('HR.urls')),
    path('prescriptions/', include('prescriptions.urls')),
    path('', include('Dashboard.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', include('News.urls')),
    path('billing/', include('Billing.urls')),
    path('education/', include('education_training.urls', namespace='education_training')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
