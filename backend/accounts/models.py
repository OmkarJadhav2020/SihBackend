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

from datetime import datetime


class Fund(models.Model):
    project = models.ForeignKey('Project', on_delete=models.CASCADE, related_name='funds')
    investigator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='funds')
    fund_amount = models.DecimalField(max_digits=15, decimal_places=2)
    gst_rate = models.DecimalField(max_digits=5, decimal_places=2, default=18.0)
    other_tax_rate = models.DecimalField(max_digits=5, decimal_places=2, default=5.0)
    gst = models.DecimalField(max_digits=15, decimal_places=2)
    other_taxes = models.DecimalField(max_digits=15, decimal_places=2)
    remaining_amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Fund for Project {self.project.id} by Investigator {self.investigator.id}"
    

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
    assigned_investigators = models.ManyToManyField(User, related_name='user_projects',blank=True)
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

from django.db import models
from .models import Project

class TimelineTask(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='timeline_tasks')
    task = models.CharField(max_length=255)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.task} ({self.status}) - Project: {self.project.title}"




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
    

# from django.db import models

# class ProjectCompletionReport(models.Model):
#     projectid = models.ForeignKey(Project,on_delete=models.CASCADE, null=True, blank=True, related_name='completionprojects')
#     projectTitle = models.CharField(max_length=255)  # Corresponds to 'projectTitle'
#     projectCode = models.CharField(max_length=100)  # Corresponds to 'projectCode'
#     startDate = models.DateField()  # Corresponds to 'startDate'
#     approvedCompletionDate = models.DateField()  # Corresponds to 'approvedCompletionDate'
#     actualCompletionDate = models.DateField()  # Corresponds to 'actualCompletionDate'
#     objectives = models.TextField()  # Corresponds to 'objectives'
#     workProgramme = models.TextField()  # Corresponds to 'workProgramme'
#     workDone = models.TextField()  # Corresponds to 'workDone'
#     objectivesFulfilled = models.TextField()  # Corresponds to 'objectivesFulfilled'
#     reasonsForNotCovering = models.TextField(blank=True, null=True)  # Corresponds to 'reasonsForNotCovering'
#     needForFurtherStudies = models.TextField(blank=True, null=True)  # Corresponds to 'needForFurtherStudies'
#     conclusions = models.TextField()  # Corresponds to 'conclusions'
#     scopeOfApplication = models.TextField()  # Corresponds to 'scopeOfApplication'
#     associatedPersons = models.TextField()  # Corresponds to 'associatedPersons'
#     expenditureStatement = models.TextField()  # Corresponds to 'expenditureStatement'

#     def __str__(self):
#         return f"{self.projectTitle} ({self.projectCode})"


from django.db import models

class ProjectRevision(models.Model):
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE, null=True, blank=True, related_name='projectREvision')
    project_name = models.CharField(max_length=255)  # Name of the project
    project_code = models.CharField(max_length=100)  # Project code
    principal_agency = models.CharField(max_length=255)  # Principal implementing agency
    project_leader = models.CharField(max_length=255)  # Project leader/coordinator
    start_date = models.DateField()  # Date of start
    completion_date = models.DateField()  # Scheduled date of completion
    approved_objective = models.TextField()  # Approved objective
    approved_work_programme = models.TextField()  # Approved work programme
    work_done_details = models.TextField()  # Details of work done
    total_approved_cost = models.DecimalField(max_digits=15, decimal_places=2)  # Total approved cost
    revised_time_schedule = models.TextField(blank=True, null=True)  # Revised time schedule
    actual_expenditure = models.DecimalField(max_digits=15, decimal_places=2)  # Actual expenditure
    revised_cost_and_justification = models.TextField()  # Revised cost and justification

    def __str__(self):
        return f"{self.project_name} ({self.project_code})"




#fund requestion
from django.db import models

class ProjectFund(models.Model):
    projectid = models.ForeignKey(Project,on_delete=models.CASCADE)
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=100)
    companyName = models.CharField(max_length=255)
    statementPeriod = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.projectName} ({self.projectCode})"

class Item(models.Model):
    project = models.ForeignKey(ProjectFund, related_name="items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    approvedCost = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fundReceived = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    interestEarned = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    expenditureIncurred = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fundProvision = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    fundRequired = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    balanceFund = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} - {self.project.projectName}"
    



from django.db import models

class EndorsementForm(models.Model):
    projectid = models.IntegerField()
    projectTitle = models.CharField(max_length=255)
    projectLeader = models.CharField(max_length=255)
    infrastructureFacilities = models.BooleanField(default=False)
    transportManpower = models.BooleanField(default=False)
    equipmentProcurement = models.BooleanField(default=False)
    financialResponsibility = models.BooleanField(default=False)
    headOfInstitution = models.CharField(max_length=255)
    seal = models.CharField(max_length=255)
    date = models.DateField()
    place = models.CharField(max_length=255)

    def __str__(self):
        return self.projectTitle



from django.db import models

class QuarterlyStatusReport(models.Model):
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255, blank=True, null=True)
    progress = models.TextField()
    principalImplementingAgency = models.CharField(max_length=255)
    subImplementingAgency = models.CharField(max_length=255)
    projectCoordinator = models.CharField(max_length=255)
    startDate = models.DateField()
    approvedCompletionDate = models.DateField()
    workDone = models.TextField()
    slippage = models.TextField(blank=True, null=True)
    correctiveActions = models.TextField()
    workNextQuarter = models.TextField()
    barChart = models.FileField(upload_to="bar_charts/")
    formIII = models.FileField(upload_to="forms/")
    formIV = models.FileField(upload_to="forms/")

    def __str__(self):
        return self.projectName



from django.db import models

class ProjectCompletionReport2(models.Model):
    projectid = models.IntegerField()
    title = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    commencementDate = models.DateField()
    approvedCompletionDate = models.DateField()
    actualCompletionDate = models.DateField()
    objectives = models.TextField()
    workProgram = models.TextField()
    workDetails = models.TextField()
    objectivesFulfilled = models.TextField()
    reasonsForSlippage = models.TextField(blank=True, null=True)
    furtherStudiesNeeded = models.TextField()
    conclusionsAndRecommendations = models.TextField()
    scopeOfApplication = models.TextField()
    associatedPersons = models.TextField()
    finalExpenditure = models.TextField(blank=True, null=True)
    formIII = models.FileField(upload_to="forms/")
    formIV = models.FileField(upload_to="forms/")

    def __str__(self):
        return self.title



from django.db import models

class ProjectExtensionReport(models.Model):
    projectid = models.IntegerField()
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    implementingAgency = models.CharField(max_length=255)
    projectLeader = models.CharField(max_length=255)
    startDate = models.DateField()
    scheduledCompletionDate = models.DateField()
    approvedObjectives = models.TextField()
    approvedWorkProgram = models.TextField()
    workDetails = models.TextField()
    revisedBarChart = models.FileField(upload_to="bar_charts/", blank=True, null=True)
    extensionReason = models.TextField()
    projectCost = models.TextField()
    actualExpenditure = models.TextField()
    formIII = models.FileField(upload_to="forms/", blank=True, null=True)
    formIV = models.FileField(upload_to="forms/", blank=True, null=True)
    formV = models.FileField(upload_to="forms/", blank=True, null=True)

    def __str__(self):
        return self.projectName





from django.db import models

class ProjectRevisionTwo(models.Model):
    projectid = models.IntegerField()
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    implementingAgency = models.CharField(max_length=255)
    projectLeader = models.CharField(max_length=255)
    startDate = models.DateField()
    scheduledCompletionDate = models.DateField()
    approvedObjective = models.TextField()
    approvedWorkProgram = models.TextField()
    workDetails = models.TextField()
    revisedCost = models.TextField()
    approvedCost = models.TextField()
    revisedSchedule = models.TextField()
    actualExpenditure = models.FloatField()
    formIII = models.FileField(upload_to="forms/", blank=True, null=True)
    formIV = models.FileField(upload_to="forms/", blank=True, null=True)
    justification = models.TextField()

    def __str__(self):
        return self.projectName



from django.db import models

class ProjectEquipment(models.Model):
    projectid = models.IntegerField()
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    principalAgency = models.CharField(max_length=255)
    subAgency = models.CharField(max_length=255)
    justification = models.TextField()

    def __str__(self):
        return self.projectName


class EquipmentDetail(models.Model):
    project = models.ForeignKey(ProjectEquipment, related_name='equipmentDetails', on_delete=models.CASCADE)
    details = models.TextField()
    noOfSets = models.IntegerField()
    makeModel = models.CharField(max_length=255)
    yearOfProcurement = models.CharField(max_length=50)
    procuredProject = models.CharField(max_length=255)
    presentCondition = models.CharField(max_length=255)
    remarks = models.TextField()

    def __str__(self):
        return self.details




from django.db import models

class ProjectManpower(models.Model):
    projectid = models.IntegerField()
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    principalAgency = models.CharField(max_length=255)
    subAgency = models.CharField(max_length=255)

    def __str__(self):
        return self.projectName


class ManpowerDetail(models.Model):
    project = models.ForeignKey(ProjectManpower, related_name='manpowerDetails', on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    noOfPersons = models.IntegerField()
    totalMonths = models.IntegerField()
    salaryPerMonth = models.DecimalField(max_digits=10, decimal_places=2)
    totalSalary = models.DecimalField(max_digits=10, decimal_places=2)
    firstYear = models.DecimalField(max_digits=10, decimal_places=2)
    secondYear = models.DecimalField(max_digits=10, decimal_places=2)
    thirdYear = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.designation





from django.db import models

class ProjectTravel(models.Model):
    projectid = models.IntegerField()
    projectName = models.CharField(max_length=255)
    projectCode = models.CharField(max_length=255)
    principalAgency = models.CharField(max_length=255)
    subAgency = models.CharField(max_length=255)

    def __str__(self):
        return self.projectName

class TravelDetail(models.Model):
    project = models.ForeignKey(ProjectTravel, related_name='travelDetails', on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)
    fromPlace = models.CharField(max_length=255)
    toPlace = models.CharField(max_length=255)
    distance = models.DecimalField(max_digits=10, decimal_places=2)
    modeFare = models.DecimalField(max_digits=10, decimal_places=2)
    noOfTrips = models.IntegerField()
    travelExpense = models.DecimalField(max_digits=10, decimal_places=2)
    noOfDays = models.IntegerField()
    daRate = models.DecimalField(max_digits=10, decimal_places=2)
    totalDA = models.DecimalField(max_digits=10, decimal_places=2)
    totalTADA = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.designation} - {self.fromPlace} to {self.toPlace}"
