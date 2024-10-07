from django import forms
from .models import Payment, Insurance

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['provider', 'policy_number', 'coverage_details', 'expiration_date', 'co_pay', 'deductible']
        widgets = {
            'expiration_date': forms.DateInput(attrs={'type': 'date'}),
        }
