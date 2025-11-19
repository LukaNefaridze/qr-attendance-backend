from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Course, Enrollment, Timetable, Session, Attendance


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
    list_display = ['code', 'name', 'professor', 'created_at']
    list_filter = ['professor', 'created_at']
    search_fields = ['code', 'name']
    readonly_fields = ['created_at', 'updated_at']


# Enrollment Admin
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at']
    list_filter = ['course', 'enrolled_at']
    search_fields = ['student__username', 'course__code', 'course__name']
    readonly_fields = ['enrolled_at']


# Timetable Admin
class TimetableAdmin(admin.ModelAdmin):
    list_display = ['course', 'day_of_week', 'start_time', 'end_time', 'room']
    list_filter = ['day_of_week', 'course']
    search_fields = ['course__code', 'course__name', 'room']
    readonly_fields = ['created_at', 'updated_at']


# Session Admin
class SessionAdmin(admin.ModelAdmin):
    list_display = ['timetable', 'started_at', 'is_active', 'expires_at']
    list_filter = ['is_active', 'started_at', 'expires_at']
    search_fields = ['timetable__course__code', 'timetable__course__name', 'qr_code']
    readonly_fields = ['started_at', 'qr_code', 'qr_secret']


# Attendance Admin
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['student', 'session', 'scanned_at', 'ip_address']
    list_filter = ['scanned_at', 'session__timetable__course']
    search_fields = ['student__username', 'session__timetable__course__code']
    readonly_fields = ['scanned_at']


# Register models
admin.site.register(User, UserAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Timetable, TimetableAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Attendance, AttendanceAdmin)