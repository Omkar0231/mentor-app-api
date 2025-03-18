from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('mentor', 'Mentor'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    email = models.EmailField(unique=True)

    username = models.CharField(max_length=150, unique=False, null=True, blank=True)  # Allow blank username

    USERNAME_FIELD = 'email'  # Use email for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.username if self.username else "Unnamed User"

