from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course


# Custom User Admin
class UserAdmin(BaseUserAdmin):
    # Fields to display in the user list
    list_display = ['username', 'email', 'is_student', 'is_professor', 'is_staff']
    list_filter = ['is_student', 'is_professor', 'is_staff']

    # Add custom fields to the edit form
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {
            'fields': ('is_student', 'is_professor'),
        }),
    )

    # Add custom fields to the "add new user" form
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Role Information', {
            'fields': ('is_student', 'is_professor'),
        }),
    )


# Course Admin
class CourseAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'professor']
    list_filter = ['professor']
    search_fields = ['code', 'name']


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)