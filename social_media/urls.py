from rest_framework import routers
from django.urls import include, path

from social_media import views


router = routers.DefaultRouter()

router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"profiles", views.ProfileViewSet, basename="profile")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social_media"
