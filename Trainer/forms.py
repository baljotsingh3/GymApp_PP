from django import forms
from Trainer.models import VideoTutorial, Trainer



class VideoTutorialForm(forms.ModelForm):
    class Meta:
        model = VideoTutorial
        fields = ['title', 'description', 'video_url', 'video_file', 'thumbnail']


class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model= Trainer
        fields= ["first_name", "last_name", "profile_picture"]