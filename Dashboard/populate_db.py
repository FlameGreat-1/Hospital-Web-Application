from django.core.management.base import BaseCommand
from Dashboard.models import Department, Staff, Expense, Payroll

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **kwargs):
        # Create departments
        dept1 = Department.objects.create(Name="HR", Staff_strength=10, Head_of_department="John Doe")
        dept2 = Department.objects.create(Name="IT", Staff_strength=20, Head_of_department="Jane Smith")

        # Create staff
        staff1 = Staff.objects.create(First_name="Alice", Last_name="Johnson", Department=dept1)
        staff2 = Staff.objects.create(First_name="Bob", Last_name="Williams", Department=dept2)

        # Create expenses
        Expense.objects.create(Department=dept1, Request_by="Alice Johnson", Amount=1000, Reason="Office supplies")

        # Create payroll entries
        Payroll.objects.create(Name=staff1, Department=dept1, Salary=50000, Position="HR Manager")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database'))
