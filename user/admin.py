from django.contrib.auth import admin
from user.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.UserAdmin):
    pass
