from django.urls import path
from .views import OTPSignView, UserListView, UserDetailView, UserUpdateView

urlpatterns = [
    path("users/signup/", OTPSignView.as_view(), name="user_signup"),
    path("users/", UserListView.as_view(), name="user_auth"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user_detail"),
    path("users/<int:pk>/update/", UserUpdateView.as_view(), name="user_update"),
]
