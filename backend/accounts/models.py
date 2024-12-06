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


class Proposal(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    duration_years = models.PositiveIntegerField()
    duration_months = models.PositiveIntegerField()
    submitted_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="investigator")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name


class ProposalImage(models.Model):
    proposal = models.ForeignKey(Proposal, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to=f'proposals/')

    def __str__(self):
        return f"Image for {self.proposal.name}"


class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    budget = models.DecimalField(max_digits=12, decimal_places=2)
    duration_years = models.PositiveIntegerField()
    duration_months = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    investigator_list = models.ManyToManyField(User, related_name='projects')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    @property
    def progress(self):
        today = datetime.now().date()
        total_days = (self.end_date - self.start_date).days
        elapsed_days = (today - self.start_date).days
        if elapsed_days > total_days:
            return 100.0
        return (elapsed_days / total_days) * 100 if total_days > 0 else 0

    def __str__(self):
        return self.name


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/')

    def __str__(self):
        return f"Image for {self.project.name}"


class Report(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='reports/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name


class Request(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, choices=REQUEST_TYPE_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return self.name


class AuditTrail(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    raised_by = models.CharField(max_length=255)  # Or use ForeignKey(User)
    completed_by = models.CharField(max_length=255, blank=True, null=True)  # Or use ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Feedback(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    owner = models.CharField(max_length=255)  # Or use ForeignKey(User)

    def __str__(self):
        return self.name
