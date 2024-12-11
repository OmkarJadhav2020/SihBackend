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



class Project(models.Model):
    
    STATUS_CHOICES = [
        ('Processing', 'Processing'),
        ('Success', 'Success'),
        ('In Review', 'In Review'),
        ('Cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    proposal = models.ForeignKey(ProjectProposal, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_projects')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Processing')
    start_date = models.DateField()
    end_date = models.DateField()
    current_progress_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    progress_status = models.TextField(null=True, blank=True)
    duration = models.CharField(max_length=50)
    assigned_investigators = models.ManyToManyField(User, related_name='user_projects')
    budget = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True,default=0)  
    funds_used = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} (ID: {self.id})"

class Report(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='reports/')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reports')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class Feedback(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    reply = models.CharField(max_length=255)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='projectname')
    feedback_image = models.FileField(upload_to='feedback', max_length=100)
    investigator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedback')

    def __str__(self):
        return self.name     
    


class FundRequisition(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='fund_requisitions')
    total_approved_cost = models.DecimalField(max_digits=15, decimal_places=2)
    total_fund_received_as_on = models.DecimalField(max_digits=15, decimal_places=2)
    interest_earned = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure_incurred_till_date = models.DecimalField(max_digits=15, decimal_places=2)
    balance_fund_available_as_on_date = models.DecimalField(max_digits=15, decimal_places=2)
    fund_provision_in_corresponding_year = models.DecimalField(max_digits=15, decimal_places=2)
    fund_required_for_year_period = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Fund Requisition for Project {self.project.title}"
    



class ExpenditureQuestion(models.Model):
    INDICATOR_CHOICES = [
        ('A', 'Land & Building'),
        ('B', 'Capital Equipment'),
        ('C', 'Manpower'),
        ('D', 'Consumable'),
        ('E', 'TA/DA'),
        ('F', 'Contingencies'),
    ]
    indicator = models.CharField(max_length=1, choices=INDICATOR_CHOICES)
    question = models.TextField()

    def __str__(self):
        return f"Indicator {self.indicator}: {self.get_indicator_display()}"

class ExpenditureStatement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="expenditure_statements")
    project_code = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="project_codes")  # Assuming same Project
    company_institute_name = models.CharField(max_length=255)
    quarter_ending = models.DateField()
    total_approved_cost = models.DecimalField(max_digits=15, decimal_places=2)
    sanctioned_provision_in_year = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure_incurred_previous_year = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure_up_to_previous_quarter = models.DecimalField(max_digits=15, decimal_places=2)
    expenditure_in_present_quarter = models.DecimalField(max_digits=15, decimal_places=2)
    progressive_expenditure_till_date = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"Expenditure Statement for {self.project}"





class QuarterlyExpenditureStatement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="quarterly_expenditures")
    project_code = models.CharField(max_length=255)
    company_institute_name = models.CharField(max_length=255)
    quarter_ending = models.DateField()

    equipment_name = models.CharField(max_length=255)
    supplier_name = models.CharField(max_length=255)
    number_of_units = models.IntegerField()
    unit_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_value = models.DecimalField(max_digits=15, decimal_places=2)
    total_approved_cost = models.DecimalField(max_digits=15, decimal_places=2)
    progressive_capital_expenditure = models.DecimalField(max_digits=15, decimal_places=2)
    building_or_land_area = models.TextField(blank=True, null=True)  # Optional for building/land details

    associate_finance_officer_name = models.CharField(max_length=255)
    associate_finance_officer_designation = models.CharField(max_length=255)
    associate_finance_officer_signature = models.ImageField(upload_to='signatures/finance_officer/', blank=True, null=True)

    project_leader_name = models.CharField(max_length=255)
    project_leader_designation = models.CharField(max_length=255)
    project_leader_signature = models.ImageField(upload_to='signatures/project_leader/', blank=True, null=True)

    def __str__(self):
        return f"Quarterly Expenditure for Project {self.project}"



class ProjectCompletionReport(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="completion_report")
    title = models.CharField(max_length=255)
    project_code = models.CharField(max_length=100)
    date_of_commencement = models.DateField()
    approved_completion_date = models.DateField()
    actual_completion_date = models.DateField()
    objectives = models.TextField()
    work_programme = models.TextField()
    details_of_work_done = models.TextField()
    objectives_fulfilled = models.TextField()
    reasons_for_incomplete_scope = models.TextField(blank=True, null=True)
    need_for_further_study = models.TextField(blank=True, null=True)
    conclusions_and_recommendations = models.TextField()
    scope_of_application = models.TextField()
    associated_persons = models.TextField()  # Names and expertise
    final_expenditure_statement = models.FileField(upload_to="completion_reports/expenditure_statements/")

    def __str__(self):
        return f"Completion Report for {self.title}"





class FinanceAnalysis(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, related_name="finance_analysis")
    total_approved_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_fund_received = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_used_cost = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    interest_earned = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    balance_available = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cost_used_last_year = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cost_used_previous_quarter = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    cost_used_till_present_quarter_end = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    overall_expenditure = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    number_of_units = models.IntegerField(default=0)
    unit_values = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Finance Analysis for Project {self.project.title}"




class IncrementRequest(models.Model):
    INCREMENT_TYPES = [
        ('Time', 'Time'),
        ('Cost', 'Cost'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="increment_requests")
    increment_type = models.CharField(max_length=10, choices=INCREMENT_TYPES)
    increment_value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)  # Can represent cost or duration
    feedback_message = models.TextField()
    feedback_image = models.ImageField(upload_to="increment_requests/", blank=True, null=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="submitted_increment_requests")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"{self.increment_type} Increment Request for Project {self.project.title}"

