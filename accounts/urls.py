from django.urls import path
from .views import OTPSignView,UserListView

urlpatterns = [
    path('users/signup/', OTPSignView.as_view(), name='user_signup'),
    path('users/', UserListView.as_view(), name='user_auth'),
]
