from django.conf import settings
from django.db import models


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    username = models.CharField(max_length=50, unique=True)
    birth_date = models.DateField(null=True, blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.username}"


class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"#{self.name}"


class Post(models.Model):
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="posts"
    )
    post_content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    media = models.ImageField(upload_to="posts/", null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    def __str__(self):
        return f"{self.author} posted: {self.post_content}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    author = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()

    def __str__(self):
        return f"{self.author} commented on {self.post}: {self.content}"


class Like(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="likes"
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="likes"
    )

    def __str__(self):
        return f"{self.user} liked {self.post}"


class Follow(models.Model):
    follower = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="following"
    )
    following = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="followers"
    )
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")

    def __str__(self):
        return f"{self.follower} follows {self.following}"
