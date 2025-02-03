from rest_framework import viewsets

from social_media.models import Comment, Follow, Like, Post, Profile, Tag
from social_media.permissions import UserProfilePermission
from social_media.serializers import (
    CommentSerializer,
    FollowSerializer,
    LikeSerializer,
    PostSerializer,
    ProfileSerializer,
    TagSerializer,
)
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (UserProfilePermission,)
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
            self.queryset = self.queryset.filter(first_name__icontains=first_name)
        
        if last_name:
            self.queryset = self.queryset.filter(last_name__icontains=last_name)
        
        if bio:
            self.queryset = self.queryset.filter(bio__icontains=bio)
        
        return self.queryset


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
