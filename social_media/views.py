import profile
import re
from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.request import Request

from social_media.models import Comment, Follow, Like, Post, Profile, Tag
from social_media.permissions import ProfilePermission, PostPermission
from social_media.serializers import (
    CommentSerializer,
    FollowSerializer,
    LikeSerializer,
    PostSerializer,
    ProfileSerializer,
    TagSerializer,
)


# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermission,)

    def get_queryset(self):
        email = self.request.GET.get("email")
        username = self.request.GET.get("username")
        first_name = self.request.GET.get("first_name")
        last_name = self.request.GET.get("last_name")
        bio = self.request.GET.get("bio")
        if email:
            self.queryset = self.queryset.filter(user__email__icontains=email)

        if username:
            self.queryset = self.queryset.filter(username__icontains=username)

        if first_name:
            self.queryset = self.queryset.filter(
                first_name__icontains=first_name
            )

        if last_name:
            self.queryset = self.queryset.filter(
                last_name__icontains=last_name
            )

        if bio:
            self.queryset = self.queryset.filter(bio__icontains=bio)

        return self.queryset

    @action(
        methods=["GET"],
        detail=False,
    )
    def my_profile(self, request, *args, **kwargs):
        profile = request.user.profile
        return HttpResponseRedirect(
            reverse("social_media:profile-detail", args=[profile.id])
        )


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)

    @action(
        methods=["POST", "GET"],
        detail=False,
    )
    def my_posts(self, request, *args, **kwargs):
        username = request.user.profile.username
        return HttpResponseRedirect(
            reverse("social_media:post-list") + f"?author={username}"
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def following_posts(self, request, *args, **kwargs):
        followings = Follow.objects.filter(follower=request.user.profile)
        self.queryset = self.queryset.filter(
            author__user__in=followings.values("following")
        )
        return super().list(request, *args, **kwargs)

    @action(
        methods=["GET"],
        detail=False,
    )
    def likes(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(likes__user__user=request.user)
        return super().list(request, *args, **kwargs)

    @action(
        methods=["GET"],
        detail=True,
    )
    def reaction(self, request, *args, **kwargs):
        post = self.get_object()
        if post.likes.filter(user=request.user.profile).exists():
            post.likes.filter(user=request.user.profile).delete()
        else:
            post.likes.create(user=request.user.profile)
        return self.retrieve(request, *args, **kwargs)

    def get_queryset(self):
        tag_data = self.request.GET.get("tag")
        content = self.request.GET.get("content")
        author = self.request.GET.get("author")

        if content:
            self.queryset = self.queryset.filter(content__icontains=content)

        if author:
            self.queryset = self.queryset.filter(
                author__username__icontains=author
            )

        if tag_data:
            tags = [tag for tag in tag_data.split(",")]
            self.queryset = self.queryset.filter(tags__name__in=tags)

        return self.queryset


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
