from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_professor = models.BooleanField(default=False)

    # Add these two lines to fix the clash:
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='core_user_set',  # Changed from default 'user_set'
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='core_user_set',  # Changed from default 'user_set'
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Course(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Enrollment(models.Model):
    """Student enrollment in courses"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments', limit_choices_to={'is_student': True})
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'course']
        verbose_name_plural = 'Enrollments'
    
    def __str__(self):
        return f"{self.student.username} - {self.course.code}"


class Timetable(models.Model):
    """Course schedule/timetable"""
    DAYS_OF_WEEK = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='timetables')
    day_of_week = models.CharField(max_length=3, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Timetables'
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.course.code} - {self.get_day_of_week_display()} {self.start_time}"


class Session(models.Model):
    """QR session for attendance"""
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE, related_name='sessions')
    qr_code = models.CharField(max_length=255, unique=True)  # HMAC-signed QR code
    qr_secret = models.CharField(max_length=255)  # Secret used for HMAC signing
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    expires_at = models.DateTimeField()  # When the QR code expires
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"Session {self.id} - {self.timetable.course.code} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"


class Attendance(models.Model):
    """Student attendance records"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendances', limit_choices_to={'is_student': True})
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='attendances')
    scanned_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)  # Optional: track IP for security
    
    class Meta:
        unique_together = ['student', 'session']  # Prevent duplicate scans
        verbose_name_plural = 'Attendances'
        ordering = ['-scanned_at']
    
    def __str__(self):
        return f"{self.student.username} - {self.session.timetable.course.code} - {self.scanned_at.strftime('%Y-%m-%d %H:%M')}"
