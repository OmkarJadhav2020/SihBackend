from django.urls import path
from .views import LoginView, UserInfoView,ProposalViewSet,GetList,ProjectViewSet,ProjectInfo,ReportView,ReportListView,ProjectCompletionReportView
from .views import *
urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('proposals/', ProposalViewSet.as_view(), name='proposal_info'),
    path('proposals/<int:proposal_id>/', ProposalViewSet.as_view(), name='proposal_delete'),
    path('getlist/', GetList.as_view(), name='getList'),
    path('projects/<int:id>/', ProjectViewSet.as_view(), name='projects'),
    path('projectinfo/', ProjectInfo.as_view(), name='projectsData'),
    path('reports/', ReportView.as_view(), name='report_info'),
    path('reportsproject/', ReportListView.as_view(), name='report_info'),
    path('project-completion-report/', ProjectCompletionReportView.as_view(),name="projectComplete") ,
    path('project-extension/', ProjectRevisionView.as_view(), name='projectRevision'),
    path('project-fund/', ProjectFundView.as_view(), name='projectRevisio1nfund'),
    path('projectfinance/', ProjectFinance2.as_view(), name='projectFund'),
    path('endorsement-form/', EndorsementFormView.as_view(), name='endorsement-form'),
    path("quarterly-status-report/", QuarterlyStatusReportView.as_view(), name="quarterly-status-report"),
    path('project-completion-report/', ProjectCompletionReportView.as_view(), name='project-completion-report'),
    path('project-extension-report/', ProjectExtensionReportView.as_view(), name='project-extension-report'),
    path('project-revision-two/', ProjectRevisionTwoView.as_view(), name='project-revision-two'),
    path('project-equipment/', ProjectEquipmentView.as_view(), name='project-equipment'),
    path('project-manpower/', ProjectManpowerView.as_view(), name='project-manpower'),
    path('project-travel/', ProjectTravelView.as_view(), name='project-travel'),
    path('addNewProject/', ProjectCreateView.as_view(), name='addProjectNew'),
    path('addTimeline',TimelineTaskView.as_view(),name='timeline'),
    path('addTimelines',TimelineTaskView1.as_view(),name='timeline1'),
    path("addFund",FundView.as_view(),name="funddetails")
    # path('audits/', AuditTrailViewSet.as_view(), name='audit_info'),
    # path('feedbacks/', FeedbackViewSet.as_view(), name='feedback_info'),
]
