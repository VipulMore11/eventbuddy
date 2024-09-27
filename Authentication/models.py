from django.db import models
from django.utils import timezone
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=10, blank=True, null=True)
    profile_pic = models.TextField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = 'User'

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

ROLE_CHOICES = [
    ('organiser', 'Organiser'),
    ('staff', 'Staff'),
]

class Organiser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='organiser')


    def __str__(self):
        return f"Organiser: {self.user.first_name} {self.user.last_name}"

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')


    def __str__(self):
        return f"Staff: {self.user.first_name} {self.user.last_name}"
