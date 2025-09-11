# Member/models.py
from django.db import models

from django.utils import timezone

from gymApp.models import GymBranch, Plan, CustomUser  # assuming you keep generic stuff in gymApp
from Trainer.models import Trainer



class Member(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)  
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    age = models.PositiveIntegerField()

    # Gym-specific
    branch = models.ForeignKey(GymBranch, null=True, on_delete=models.SET_NULL)
    assigned_trainer = models.ForeignKey(Trainer, null=True, blank=True, on_delete=models.SET_NULL)
    plan = models.ForeignKey(Plan, null=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(
        upload_to='Members/profile_pictures/',
        blank=True,
        null=True,
        max_length= 500,
        default='https://lnbamhwkbhfxoeltsoqt.supabase.co/storage/v1/object/public/media-files/trainers/profile_pictures/default.png'
    )
    start_date = models.DateField(default=timezone.now)
    height_cm = models.FloatField(null=True, blank=True)
    weight_kg = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Member: {self.user.username} ({self.first_name} {self.last_name})"


class Payment(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True, blank=True)
    
    order_id = models.CharField(max_length=100, unique=True, blank=True, null=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)  # After success
    signature = models.CharField(max_length=255, null=True, blank=True)  # After success

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="INR")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[("created", "Created"), ("paid", "Paid"), ("failed", "Failed")],
        default="created"
    )

    def __str__(self):
        return f"Payment {self.order_id} - {self.member.user.username} ({self.status})"



class Invoice(models.Model):
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to="invoices/")
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice for Payment {self.payment.payment_id}"

