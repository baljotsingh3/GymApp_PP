from django.urls import path
from Trainer.views import *

app_name = "Trainer"


urlpatterns = [
    
    path("profile/", ProfileView.as_view(), name="trainer_profile"),
    path("tables/", CoachPanelView.as_view(), name="coach_panel"),
  
    path("dashboard/", TrainerDashboardView.as_view(), name="trainer_dashboard"),
    
    path('add-video/', add_video, name='add_video'),
    path('edit-video/<int:pk>/', edit_video, name='edit_video'),
    path('delete-video/<int:pk>/', delete_video, name='delete_video'),
    path('video-list/', video_list, name='video_list'),
]