from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class ProfilePermission(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method in ["GET"] or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.method in ["GET"]


class PostPermission(BasePermission):
    def has_permission(self, request: Request, view):
        return request.method in ["GET"] or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author.user == request.user or request.method in ["GET"]
