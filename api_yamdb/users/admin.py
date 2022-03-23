from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'username',
        'first_name',
        'last_name',
        'bio',
        'role',
        'email',
        'is_staff',
        'is_active'
    )

admin.site.register(User, UserAdmin)