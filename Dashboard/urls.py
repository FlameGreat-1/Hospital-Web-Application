from django.urls import path
from . import views

app_name = 'Dashboard'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('departments_list/', views.department_list, name='department_list'),
    path('staff/', views.staff_list, name='staff_list'),
    path('expenses/', views.expense_list, name='expense_list'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('messages/', views.message_list, name='message_list'),
    path('approve-expense/<int:expense_id>/', views.approve_expense, name='approve_expense'),
]
