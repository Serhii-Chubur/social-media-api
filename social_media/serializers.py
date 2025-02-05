from social_media.models import Follow, Like, Post, Profile, Tag, Comment
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    is_active = serializers.BooleanField(
        source="user.is_active", read_only=True
    )

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class ProfileListSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    is_active = serializers.BooleanField(
        source="user.is_active", read_only=True
    )

    class Meta:
        model = Profile
        fields = ("id", "username", "email", "profile_picture", "is_active")


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagRetrieveSerializer(serializers.ModelSerializer):
    name = serializers.StringRelatedField(source="__str__")

    class Meta:
        model = Tag
        fields = ("name",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    add_your_tags = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("author",)

    def create(self, validated_data):
        author = self.context["request"].user.profile
        validated_data["author"] = author
        if "add_your_tags" in validated_data:
            tags = [
                tag.strip()
                for tag in validated_data.pop("add_your_tags").split(",")
            ]
            for tag in tags:
                new_tag, _ = Tag.objects.get_or_create(name=tag)
                validated_data["tags"].append(new_tag)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "add_your_tags" in validated_data:
            tags = [
                tag.strip()
                for tag in validated_data.pop("add_your_tags").split(",")
            ]
            for tag in tags:
                new_tag, _ = Tag.objects.get_or_create(name=tag)
                validated_data["tags"].append(new_tag)
        return super().update(instance, validated_data)


class PostListSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source="likes.count", read_only=True)
    tags = TagRetrieveSerializer(many=True)
    author = serializers.CharField(source="author.username", read_only=True)


    class Meta:
        model = Post
        fields = "id", "likes", "tags", "post_content", "author"
        read_only_fields = ("author",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user.profile
        return super().create(validated_data)


class CommentInPostSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    class Meta:
        model = Comment
        fields = ("author", "content",)

    def create(self, validated_data):
        return super().create(validated_data)


class CommentPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    comment = CommentInPostSerializer(many=False, write_only=True)
    post_content = serializers.CharField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "post_content",
            "comments",
            "comment",
        )

    def create(self, validated_data):
        comment_data = validated_data.pop("comment")
        post = self.context["post"]
        author = self.context["request"].user.profile
        Comment.objects.create(author=author, post=post, **comment_data)
        return post


class LikeRetrieveSerializer(serializers.ModelSerializer):
    info = serializers.StringRelatedField(source="__str__")

    class Meta:
        model = Like
        fields = ("info",)


class PostRetrieveSerializer(serializers.ModelSerializer):
    tags = TagRetrieveSerializer(many=True)
    comments = CommentInPostSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(source="likes.count", read_only=True)
    liked_users = LikeRetrieveSerializer(source="likes", many=True, read_only=True)
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = "__all__"

    def validate(self, attrs):
        follower = attrs["follower"]
        following = attrs["following"]
        if follower == following:
            raise serializers.ValidationError("You cannot follow yourself")
        return super().validate(attrs)
