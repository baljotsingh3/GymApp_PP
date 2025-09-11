# Trainer/models.py
from django.db import models

from gymApp.models import CustomUser



class Trainer(models.Model):
    
    # Specialization as choice field
    SPECIALIZATIONS = [
        ('yoga', 'Yoga'),
        ('strength', 'Strength Training'),
        ('cardio', 'Cardio'),
        ('crossfit', 'CrossFit'),
        ('pilates', 'Pilates'),
        # Add more as needed
    ]
    
    User = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=254)
    # Phone number
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    profile_picture = models.ImageField(
        upload_to='trainers/profile_pictures/',
        blank=True,
        null=True,
        max_length= 500,
        default='https://utpzvsvgktqppalcpvkn.supabase.co/storage/v1/object/sign/GymApp/media/default.png?token=eyJraWQiOiJzdG9yYWdlLXVybC1zaWduaW5nLWtleV9iNWEwNDA3MS1iNTU5LTRmYzMtYjZhOC02MTZjMGI4OTE3NDkiLCJhbGciOiJIUzI1NiJ9.eyJ1cmwiOiJHeW1BcHAvbWVkaWEvZGVmYXVsdC5wbmciLCJpYXQiOjE3NTc1MjY3NzcsImV4cCI6MTc4OTA2Mjc3N30.1VfW6hH7TfAFcQtz2YzwxMiy9Ldj9domHDSMaspN91w'
    )
    
    
    specialization = models.CharField(
        max_length=50,
        choices=SPECIALIZATIONS,
        default='strength'
    )
    # Experience in years
    experience_years = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Trainer: {self.User.username} ({self.first_name} {self.last_name})"


class VideoTutorial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    video_url = models.URLField(blank=True, null=True)  # if embedding from YouTube or Vimeo
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)  # for direct upload
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Trainer, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title