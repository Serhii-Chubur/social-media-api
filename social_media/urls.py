from rest_framework import routers
from django.urls import include, path

from social_media import views


router = routers.DefaultRouter()

router.register(r"posts", views.PostViewSet, basename="post")
router.register(r"likes", views.LikeViewSet, basename="like")
router.register(r"comments", views.CommentViewSet, basename="comment")
router.register(r"follows", views.FollowViewSet, basename="follow")
router.register(r"profiles", views.ProfileViewSet, basename="profile")
router.register(r"tags", views.TagViewSet, basename="tag")

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "social_media"
