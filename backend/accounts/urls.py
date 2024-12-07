from django.urls import path
from .views import LoginView, UserInfoView,ProposalViewSet,GetList

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserInfoView.as_view(), name='user_info'),
    path('proposals/', ProposalViewSet.as_view(), name='proposal_info'),
    path('getlist/', GetList.as_view(), name='getList'),
    # path('projects/', ProjectViewSet.as_view(), name='project_info'),
    # path('reports/', ReportViewSet.as_view(), name='report_info'),
    # path('requests/', RequestViewSet.as_view(), name='request_info'),
    # path('audits/', AuditTrailViewSet.as_view(), name='audit_info'),
    # path('feedbacks/', FeedbackViewSet.as_view(), name='feedback_info'),
]
