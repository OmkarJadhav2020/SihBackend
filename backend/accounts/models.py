from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLES = [
        ('admin', 'Admin'),
        ('investigator', 'Investigator'),
        ('researcher', 'Researcher'),
        ('review_committee', 'Review Committee'),
    ]
    role = models.CharField(max_length=20, choices=ROLES)

# class Proposal(models.Model):
#     title = models.CharField(max_length=200)
#     description = models.TextField()
#     investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='proposals')
#     status = models.CharField(max_length=50, default='Pending')
#     created_at = models.DateTimeField(auto_now_add=True)

# class Project(models.Model):
#     proposal = models.OneToOneField(Proposal, on_delete=models.CASCADE)
#     milestones = models.TextField()
#     budget = models.FloatField()
#     status = models.CharField(max_length=50, default='Ongoing')
#     created_at = models.DateTimeField(auto_now_add=True)

# class AuditTrail(models.Model):
#     action = models.CharField(max_length=200)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
#     timestamp = models.DateTimeField(auto_now_add=True)

