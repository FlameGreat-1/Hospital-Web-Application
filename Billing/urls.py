from django.urls import path
from . import views

app_name = 'Billing'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('make-payment/<int:bill_id>/', views.make_payment, name='make_payment'),
    path('insurance-info/', views.insurance_info, name='insurance_info'),
    path('payment-history/', views.payment_history, name='payment_history'),
    path('webhook/', views.payment_webhook, name='payment_webhook'),
    path('bill/<int:bill_id>/', views.bill_detail, name='bill_detail'),
]
