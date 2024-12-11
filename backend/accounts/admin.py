from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.ProjectProposal)
# admin.site.register(models.ProposalImage)
admin.site.register(models.Project)
# admin.site.register(models.ProjectImage)
admin.site.register(models.Report)

admin.site.register(models.Feedback)
admin.site.register(models.FundRequisition)
admin.site.register(models.ExpenditureQuestion)
admin.site.register(models.ExpenditureStatement)
admin.site.register(models.QuarterlyExpenditureStatement)
admin.site.register(models.ProjectCompletionReport)
admin.site.register(models.FinanceAnalysis)
