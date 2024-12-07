from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('investigator', 'Investigator'),
        ('researcher', 'Researcher'),
        ('review_committee', 'Review Committee'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)



# Common choices
STATUS_CHOICES = [
    ('Pending', 'Pending'),
    ('Under Investigation', 'Under Investigation'),
    ('Approved', 'Approved'),
]

REQUEST_TYPE_CHOICES = [
    ('Money', 'Money'),
    ('Duration', 'Duration'),
]

class ProjectProposal(models.Model):
    # Form data
    agency_name = models.CharField(max_length=255)
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='coordinator_projects')
    sub_agency = models.CharField(max_length=255, blank=True, null=True)
    co_investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='co_investigator_projects', blank=True, null=True)
    issue_definition = models.TextField()
    objective = models.TextField()
    justification_area = models.TextField()
    coal_benefit = models.TextField()
    subject_justification = models.TextField()
    work_plan = models.TextField()
    methodology = models.TextField()
    organization = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    approved = models.BooleanField(default=False)
    # Table data 
    capital_expenditure = models.DecimalField(max_digits=10, decimal_places=2)
    total_capital = models.DecimalField(max_digits=10, decimal_places=2)
    salaries = models.DecimalField(max_digits=10, decimal_places=2)
    consumables = models.DecimalField(max_digits=10, decimal_places=2)
    travel = models.DecimalField(max_digits=10, decimal_places=2)
    workshops = models.DecimalField(max_digits=10, decimal_places=2)
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Project Proposal by {self.agency_name} - {self.coordinator.username}"
