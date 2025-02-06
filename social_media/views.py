from django.http import HttpResponseRedirect
from django.urls import reverse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from social_media.models import Comment, Follow, Like, Post, Profile, Tag
from social_media.permissions import ProfilePermission, PostPermission
from social_media.serializers import (
    CommentPostSerializer,
    CommentSerializer,
    FollowSerializer,
    LikeRetrieveSerializer,
    PostListSerializer,
    PostRetrieveSerializer,
    PostSerializer,
    ProfileListSerializer,
    ProfileSerializer,
    TagSerializer,
)


# Create your views here.
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (ProfilePermission,)

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer
        return super().get_serializer_class()

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
        """
        Retrieve the profile of the current user.

        This action handles GET requests to retrieve the profile data
        of the current user. The user is redirected to the profile
        detail page after the action.
        """

        profile = request.user.profile
        return HttpResponseRedirect(
            reverse("social_media:profile-detail", args=[profile.id])
        )

    @action(
        methods=["GET"],
        detail=False,
    )
    def followings(self, request, *args, **kwargs):
        """
        Retrieve a list of users the current user is following.

        This action handles GET requests to retrieve a list of users that the
        current user is following. The users are filtered based on the follow
        relationships of the current user's profile.
        """
        followings = Follow.objects.filter(follower=request.user.profile)
        self.queryset = self.queryset.filter(
            user__profile__in=followings.values("following")
        )
        return super().list(request, *args, **kwargs)

    @action(
        methods=["GET"],
        detail=False,
    )
    def followers(self, request, *args, **kwargs):
        """
        Retrieve a list of users following the current user.

        This action handles GET requests to retrieve a list of users that are
        following the current user. The users are filtered based on the follow
        relationships of the current user's profile.
        """
        followers = Follow.objects.filter(following=request.user.profile)
        self.queryset = self.queryset.filter(
            user__profile__in=followers.values("follower")
        )
        return super().list(request, *args, **kwargs)

    @action(
        methods=["GET"],
        detail=True,
    )
    def follow(self, request, *args, **kwargs):
        """
        Toggle a follow relationship
        between the current user and the profile.

        This action handles GET requests to toggle a follow relationship
        between the current user and the profile.
        If the follow relationship does not exist,
        a new follow relationship is created.
        If the follow relationship exists,
        the follow relationship is deleted.
        """

        profile = self.get_object()
        user = request.user.profile

        follow_data = {
            "follower": user.id,
            "following": profile.id,
        }

        serializer = FollowSerializer(data=follow_data)
        serializer.is_valid(raise_exception=True)

        relation = Follow.objects.filter(follower=user, following=profile)

        if not relation.exists():
            Follow.objects.create(follower=user, following=profile)
        else:
            relation.delete()
        return HttpResponseRedirect(
            reverse("social_media:profile-detail", args=[profile.id])
        )

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="email",
                description="Filter by email",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="username",
                description="Filter by username",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="first_name",
                description="Filter by first_name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="last_name",
                description="Filter by last_name",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="bio",
                description="Filter by bio",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of profiles.

        Filters the profiles based on optional query parameters such as
        'email', 'username', 'first_name', 'last_name', and 'bio'. Returns the
        filtered list of profiles.
        """
        return super().list(request, *args, **kwargs)

    @extend_schema()
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific profile by its ID.

        This method handles GET requests
        to retrieve a detailed representation of a specific
        profile. It utilizes the ProfileSerializer
        to serialize the retrieved profile data
        and returns the detailed profile information
        with a status indicating success.
        """

        return super().retrieve(request, *args, **kwargs)

    @extend_schema()
    def create(self, request, *args, **kwargs):
        """
        Create a new profile.

        This method handles POST requests
        to create a new profile.
        It utilizes the ProfileSerializer to validate
        and deserialize the incoming data.
        Upon successful creation,
        it returns a serialized representation of the
        newly created profile with a status indicating success.
        """
        return super().create(request, *args, **kwargs)

    @extend_schema()
    def update(self, request, *args, **kwargs):
        """
        Update a specific profile by its ID.

        This method handles PUT requests to update
        an existing profile. It utilizes
        the ProfileSerializer to validate and
        deserialize the incoming data.
        Upon successful update, it returns a serialized
        representation of the updated
        profile with a status indicating success.
        """

        return super().update(request, *args, **kwargs)

    @extend_schema()
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a specific profile by its ID.

        This method handles PATCH requests
        to partially update an existing profile.
        It utilizes the ProfileSerializer
        to validate and deserialize the incoming data.
        Upon successful partial update,
        it returns a serialized representation of the
        partially updated profile with a status indicating success.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema()
    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific profile by its ID.

        This method handles DELETE requests
        to delete an existing profile.
        It returns a status indicating success
        upon successful deletion.
        """
        return super().destroy(request, *args, **kwargs)


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (PostPermission,)

    def get_serializer_class(self):
        if self.action == "list":

            return PostListSerializer
        if self.action == "retrieve":
            return PostRetrieveSerializer
        if self.action == "comment":
            return CommentPostSerializer

        return PostSerializer

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

    @action(
        methods=["POST", "GET"],
        detail=False,
    )
    def my_posts(self, request, *args, **kwargs):
        """
        Retrieve a list of posts by the current user.

        This method handles GET and POST requests
        to retrieve a list of posts created
        by the current user.
        It redirects to the post list with the query parameter
        'author' set to the username of the current user.
        """
        username = request.user.profile.username
        return HttpResponseRedirect(
            reverse("social_media:post-list") + f"?author={username}"
        )

    @action(
        methods=["GET", "POST"],
        detail=False,
    )
    def following_posts(self, request, *args, **kwargs):
        """
        Retrieve a list of posts from users
        the current user is following.

        This action handles GET and POST
        requests to fetch posts authored by users
        whom the current user is following.
        The posts are filtered based on the
        follow relationships of the current user's profile.
        """

        followings = Follow.objects.filter(follower=request.user.profile)
        self.queryset = self.queryset.filter(
            author__user__in=followings.values("following")
        )
        return super().list(request, *args, **kwargs)

    @action(
        methods=["GET", "POST"],
        detail=False,
    )
    def likes(self, request, *args, **kwargs):
        """
        Retrieve a list of posts the current user has liked.

        This method handles GET requests to retrieve a list of posts that the
        current user has liked. The posts are filtered based on the like
        relationships of the current user's profile.
        """
        likes_data = self.queryset.filter(likes__user__user=request.user)
        serializer = PostRetrieveSerializer(likes_data, many=True)
        return Response(serializer.data)

    @action(
        detail=True,
    )
    def reaction(self, request, *args, **kwargs):
        """
        Toggle a like on a post for the current user.

        This action allows the current user to like or unlike a specific post.
        If the post is already liked by the user, the like is removed.
        If the post is not liked by the user, a new like is created.
        Redirects the user to the post detail page after the action.
        """

        post = self.get_object()
        if post.likes.filter(user=request.user.profile).exists():
            post.likes.filter(user=request.user.profile).delete()
            return HttpResponseRedirect(
                reverse("social_media:post-detail", args=[post.id])
            )

        else:
            post.likes.create(user=request.user.profile)
            return HttpResponseRedirect(
                reverse("social_media:post-detail", args=[post.id])
            )

    @action(methods=["GET", "POST"], detail=True)
    def comment(self, request, *args, **kwargs):
        """
        Get or create a comment on a post.

        GET requests retrieve the comments on the post.
        POST requests create a new comment on the post.

        The request should contain the content of the comment in the body.
        The comment is validated and saved to the database.
        If the comment is invalid, a 400 response is returned with the
        serializer errors.
        If the comment is valid, a 200 response is returned with the
        post data including the new comment.
        The user is redirected to the post detail page.
        """
        self.permission_classes = (IsAuthenticated,)
        post = self.get_object()
        if request.method == "POST":
            serializer = CommentPostSerializer(
                data=request.data, context={"request": request, "post": post}
            )
            if serializer.is_valid():
                serializer.save()
                return HttpResponseRedirect(
                    reverse("social_media:post-detail", args=[post.id])
                )
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        post_serializer = PostRetrieveSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="tag",
                description="Filter by tag",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="author",
                description="Filter by author",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="content",
                description="Filter by content",
                required=False,
                type=str,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of posts.

        Filters the posts based on optional query parameters such as 'content',
        'author', and 'tag'. Returns the filtered list of posts.
        """

        return super().list(request, *args, **kwargs)

    @extend_schema()
    def create(self, request, *args, **kwargs):
        """
        Handle POST requests for creating a post.

        This method processes incoming POST requests to create a new post.
        It utilizes the PostSerializer
        to validate and deserialize the incoming data.
        Upon successful creation,
        it returns a serialized representation of the newly
        created post with a status indicating success.
        """

        return super().create(request, *args, **kwargs)

    @extend_schema()
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific post by its ID.

        This method handles GET requests
        to retrieve a detailed representation of a specific post.
        It utilizes the PostRetrieveSerializer
        to serialize the retrieved post data and returns
        the detailed post information with a status indicating success.
        """

        return super().retrieve(request, *args, **kwargs)

    @extend_schema()
    def update(self, request, *args, **kwargs):
        """
        Update a specific post by its ID.

        This method handles PUT requests
        to update an existing post.
        It utilizes the PostSerializer
        to validate and deserialize the incoming data.
        Upon successful update,
        it returns a serialized representation of the updated
        post with a status indicating success.
        """
        return super().update(request, *args, **kwargs)

    @extend_schema()
    def partial_update(self, request, *args, **kwargs):
        """
        Partially update a specific post by its ID.

        This method handles PATCH requests
        to partially update an existing post.
        It utilizes the PostSerializer
        to validate and deserialize the incoming data.
        Upon successful partial update,
        it returns a serialized representation of the
        partially updated post with a status indicating success.
        """
        return super().partial_update(request, *args, **kwargs)

    @extend_schema()
    def destroy(self, request, *args, **kwargs):
        """
        Delete a specific post by its ID.

        This method handles DELETE requests
        to delete an existing post. It returns
        a status indicating success upon successful deletion.
        """
        return super().destroy(request, *args, **kwargs)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeRetrieveSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
