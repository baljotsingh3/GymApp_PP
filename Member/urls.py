
from django.contrib import admin
from django.urls import path, include
from .views import *

from django.contrib.auth.views import LogoutView

app_name = "Member"


urlpatterns = [
    path("dashboard/", MemberDashboardView.as_view(), name="member_dashboard"),
    path("profile/", MemberProfileView.as_view(), name="member_profile"),
    #path("edit-profile/", update_profile, name="edit_profile"),

    path("AI-trainer/", ChatBotView.as_view(), name="chatbot"),
    
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="Member:login"), name="logout"),
    
    
    path("billing/", BillingHistory.as_view() , name="billing"),
    path("payment_form/", PaymentForm.as_view() , name="payment_card"),
]


