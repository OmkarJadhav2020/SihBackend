from django.urls import path
from .views import LoginView, UserInfoView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('me/', UserInfoView.as_view(), name='user_info'),
]
