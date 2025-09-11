from django.urls import path
from . import views


app_name = "gymApp"

urlpatterns = [
    #path("register/", views.signup_view, name= "register"),
    
    path("", views.home, name="home"),
    path("contact/", views.contact, name= 'contact'),
    
    path("video_list/", views.video_list , name= "video_list"),
    path("video_detail/<int:pk>/", views.video_detail, name="video_detail"),
    
    path('blogs/', views.public_blog_list, name='public_blog_list'),
    
]
