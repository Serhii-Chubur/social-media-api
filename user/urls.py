from user import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="create_user"),
    path("me/", views.ManageUserView.as_view(), name="manage_user"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "user/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "user/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("user/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
