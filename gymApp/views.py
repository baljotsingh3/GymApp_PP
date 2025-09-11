from django.shortcuts import render, get_object_or_404,redirect 
from django.contrib import messages

from Trainer.models import *
from Blog.models import *

from django.core.paginator import Paginator
from gymApp.forms import *

from Member.payment.services import EmailService




def home(request):
    
    blogs = Blog.objects.order_by('-created_at')[:2]  # Fetch latest 2 blogs
    return render(request, "gymApp/index.html", {'blogs': blogs})

def contact(request):
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data — e.g., save it, email it, etc.
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            email= EmailService()
            email.send_simple_email(subject,message)
            # Example: just showing a success message
            messages.success(request, "Your message has been sent!")
            return redirect('gymApp:contact')  # redirect to avoid resubmission
        
    else:
        form = ContactForm()
    
    return render(request, 'gymApp/contact.html', {'form': form})
    
    


def public_blog_list(request):
    
    blogs = Blog.objects.all().order_by('-created_at')  # latest first
    return render(request, 'gymApp/public_blog_list.html', {'blogs': blogs})




# 

def video_list(request):
    videos = VideoTutorial.objects.all().order_by('-created_at')
    return render(request, 'gymApp/video_list.html', {'videos': videos})

def video_detail(request, pk):
    video = get_object_or_404(VideoTutorial, pk=pk)
    return render(request, 'gymApp/video_detail.html', {'video': video})