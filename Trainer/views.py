from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.decorators import login_required
from .mixins import *

from Trainer.forms import *
from Trainer.models import *
from Member.models import Member
from Blog.models import *

from django.contrib import messages

# from Member.utils.storages import upload_media
  # Import your models

class ProfileView(LoginRequiredMixin, GroupRequiredMixin, View):
    template_name = "Trainer/profile.html"
    login_url = 'Member:login'
    group_required = 'Trainer'  # Only trainers can access
    
    
    def get(self, request):
        try:
            trainer = request.user.trainer  # Access Trainer instance
        except Trainer.DoesNotExist:
            # Handle case where trainer profile does not exist
            trainer = None
        
        # Get trainer's blogs if applicable
        blogs = Blog.objects.filter(author=request.user).order_by('-created_at') if trainer else []
        
        user_chats = CustomUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
        
        context = {
            "trainer": trainer,
            "blogs": blogs,
            
            "user_chats": user_chats,
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        try:
            trainer = request.user.trainer
        except Trainer.DoesNotExist:
            return redirect('Member:login')

        action = request.POST.get('action')
        
        profile_picture = request.FILES.get("profile_picture")
        
        # file_name= r'media/trainers/profile_pictures/001.png'
        # uploaded_path_dp= upload_media(profile_picture,file_name)
        
        if profile_picture:
            trainer.profile_picture = profile_picture

        if action == "update_profile":
            return self.update_profile(request, trainer)
        elif action == "custom_function":
            return self.custom_function(request, trainer)
        else:
            messages.error(request, "Unknown action")
            return redirect("Trainer:trainer_profile")

    def update_profile(self, request, trainer):
        # Update basic info
        trainer.first_name = request.POST.get("first_name", trainer.first_name)
        trainer.last_name = request.POST.get("last_name", trainer.last_name)
        trainer.phone_number = request.POST.get("phone_number", trainer.phone_number)
        trainer.specialization = request.POST.get("specialization", trainer.specialization)

        # Update profile picture
        profile_picture = request.FILES.get("profile_picture")
        
        # file_name= r'media/trainers/profile_pictures/001.png'
        # uploaded_path_dp= upload_media(profile_picture,file_name)
        
        if profile_picture:
            trainer.profile_picture = profile_picture

        trainer.save()
        messages.success(request, "Profile updated successfully!")
        return redirect("Trainer:trainer_profile")


    def custom_function(self, request, trainer):
        # Example custom logic
        # This could be anything: sending a welcome email, triggering a stats calculation, etc.
        result = f"Hello {trainer.first_name}, custom function executed!"
        messages.info(request, result)
        return redirect("Trainer:profile")






class TrainerDashboardView(ProfileView):
    template_name= template_name = "Trainer/dashboard.html"
    


class CoachPanelView(ProfileView):
    template_name = "Trainer/tables.html"

    def get(self, request):
        
        try:
            trainer_profile = self.request.user.trainer
        except Trainer.DoesNotExist:
            return redirect('gymApp:home')  # Not a trainer
        
        videos = VideoTutorial.objects.filter(author=trainer_profile).order_by('-created_at')
        
        trainer = Trainer.objects.get(User=request.user)
        
        assigned_members = Member.objects.filter(assigned_trainer=trainer)
        
       
        context= { 
            'videos': videos,
            'assigned_members': assigned_members, 
                
            }
        
        return render(request, self.template_name, context)




@login_required
def add_video(request):
    if not request.user.groups.filter(name='Trainer').exists():
        return redirect('gymApp:home')  # Only trainers allowed

    if request.method == "POST":
        form = VideoTutorialForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            
            video.author = request.user.trainer
            video.save()
            return redirect('Trainer:trainer_profile')  # Redirect back to profile
    else:
        form = VideoTutorialForm()
    
    return render(request, 'Trainer/add_video.html', {'form': form})
login_required
def edit_video(request, pk):
    try:
        trainer_profile = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('gymApp:home')  # Not a trainer

    # Correct: author expects Trainer instance
    video = get_object_or_404(VideoTutorial, pk=pk, author=trainer_profile)

    if request.method == "POST":
        form = VideoTutorialForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect('Trainer:trainer_profile')
    else:
        form = VideoTutorialForm(instance=video)

    return render(request, 'Trainer/edit_video.html', {'form': form, 'video': video})


@login_required
def video_list(request):
    try:
        trainer_profile = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('gymApp:home')  # Not a trainer

    # Get all videos uploaded by this trainer
    videos = VideoTutorial.objects.filter(author=trainer_profile).order_by('-created_at')

    context = {
        'videos': videos
    }
    return render(request, 'Trainer/video_list.html', context)

login_required
def delete_video(request, pk):
    try:
        trainer_profile = request.user.trainer
    except Trainer.DoesNotExist:
        return redirect('gymApp:home')

    video = get_object_or_404(VideoTutorial, pk=pk, author=trainer_profile)
    video.delete()
    return redirect('Trainer:video_list')