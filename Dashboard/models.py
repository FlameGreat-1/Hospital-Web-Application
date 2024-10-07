from django.db import models
from django.contrib.auth.models import User


class Department(models.Model):
    duration = (
        ("JANUARY_MARCH", "january_march"),
        ("APRIL_JUNE", "april_june"),
        ("JULY_SEPTEMBER", "july_september"),
        ("OCTOBER_DECEMBER", "october_december")
    )
    Name = models.CharField(max_length=100)
    Staff_strength = models.PositiveIntegerField()
    Head_of_department = models.CharField(max_length=100)
    Income_generated = models.PositiveIntegerField(blank=True, null=True)
    Expenses = models.PositiveIntegerField(blank=True, null=True)
    Duration = models.CharField(choices=duration, max_length=50)
    Function = models.CharField(max_length=250)

    def __str__(self):
        return self.Name


class Staff(models.Model):
    First_name = models.CharField(max_length=100)
    Last_name = models.CharField(max_length=100)
    Phone_number = models.PositiveIntegerField()
    email = models.EmailField()
    Reference = models.CharField(max_length=11)
    Reference_phone_number = models.PositiveIntegerField()
    Home_address = models.CharField(max_length=100)
    State = models.CharField(max_length=100)
    Age = models.PositiveIntegerField(blank=True, null=True)
    Country = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    Salary = models.PositiveIntegerField(blank=True, null=True)
    On_probation = models.BooleanField(default=True)
    Number_of_queries = models.PositiveIntegerField(blank=True, null=True)
    Department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    Joined = models.DateField()
    Resigned = models.DateField(blank=True, null=True)

    def __str__(self):
        # Return both first and last name to avoid issues
        return f"{self.First_name} {self.Last_name}"


class Expense(models.Model):
    Department = models.ForeignKey(Department, on_delete=models.CASCADE)
    Request_by = models.CharField(max_length=100)
    Position = models.CharField(max_length=100)
    Amount = models.PositiveIntegerField()
    Reason = models.CharField(max_length=250)
    Approved = models.BooleanField(default=False)
    Approved_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    Date = models.DateField()

    def __str__(self):
        return str(self.Department)


class Payroll(models.Model):
    Name = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    Department = models.ForeignKey(Department, on_delete=models.DO_NOTHING)
    Salary = models.PositiveIntegerField()
    Position = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.Name.First_name} {self.Name.Last_name}"  # Return a string representation of the Staff object



class Message(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Phone_number = models.PositiveIntegerField()
    Address = models.CharField(max_length=250)
    Message = models.TextField()