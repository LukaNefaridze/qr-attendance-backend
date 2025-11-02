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

    def __str__(self):
        return f"{self.code} - {self.name}"
