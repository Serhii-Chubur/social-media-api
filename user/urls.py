from user import views
from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView
)


urlpatterns = [
    path("register/", views.CreateUserView.as_view(), name="create_user"),
    path("me/", views.ManageUserView.as_view(), name="manage_user"),
    # path("logout/", views.logout, name="logout"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "token/", TokenObtainPairView.as_view(), name="token_obtain_pair"
    ),
    path(
        "token/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('api/token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
]

app_name = "user"
