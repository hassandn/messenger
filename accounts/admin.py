from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('phone', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined')
    search_fields = ('phone', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

admin.site.register(User, UserAdmin)
