from social_media.models import Comment, Follow, Like, Post, Profile, Tag
from django.contrib import admin

# Register your models here.
admin.site.register(Profile)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
