from social_media.models import Follow, Like, Post, Profile, Tag, Comment
from rest_framework import serializers


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("user",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["user"] = user
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class PostSerializer(serializers.ModelSerializer):
    likes = serializers.IntegerField(source = "likes.count", read_only=True)


    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ("author",)

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["author"] = user.profile
        return super().create(validated_data)


class CommentInPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("content",)
    
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
        Comment.objects.create(author=author,post=post, **comment_data)
        return post



class PostRetrieveSerializer(serializers.ModelSerializer):
    comments = CommentInPostSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(source = "likes.count", read_only=True)

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
