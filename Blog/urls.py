# blog/urls.py
from django.urls import path
from . import views


app_name= "Blog"

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    
    
    #for_profile_view
    path('<int:pk>/', views.member_personal_blog_detail, name='blog_detail'),
    
    path('new/', views.blog_create, name='blog_create'),
    path('<int:pk>/edit/', views.blog_edit, name='blog_edit'),
    path('<int:pk>/delete/', views.blog_delete, name='blog_delete'),
]
