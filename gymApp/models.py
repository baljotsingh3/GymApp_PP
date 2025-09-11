# gymApp/models.py
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models



class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=False)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'   # authentication happens with email
    REQUIRED_FIELDS = ['username']  # keep username for profile, not login

    def __str__(self):
        return f"{self.username} ({self.email})"


class GymBranch(models.Model):
    # Optional: predefined branch names
    BRANCH_CHOICES = [
        ('Golden', 'Golden Gym'),
        ('Jora', 'Jorawar Fitness'),
    ]
    name = models.CharField(
        max_length=50,
        choices=BRANCH_CHOICES,
        default='Jora'
    )
    
    # Optional: predefined locations, or just leave free-text
    LOCATION_CHOICES = [
        ('59', 'Sector 59'),
        ('7', 'Phase 7'),
    ]
    location = models.CharField(
        max_length=100,
        choices=LOCATION_CHOICES,
        default='Phase 7'
    )

    def __str__(self):
        return f"{self.get_name_display()} ({self.get_location_display()})"



class Plan(models.Model):
    # If you want predefined plan names
    PLAN_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
        ('pro', 'Pro'),
    ]
    
    name = models.CharField(
        max_length=50,
        choices=PLAN_CHOICES,
        default='basic'
    )
    # Duration can also have choices, optional
    DURATION_CHOICES = [
        (1, '1 month'),
        (3, '3 months'),
        (6, '6 months'),
        (12, '12 months'),
    ]
    duration_months = models.PositiveIntegerField(choices=DURATION_CHOICES, default=1)
    
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.get_name_display()} - {self.get_duration_months_display()}"


