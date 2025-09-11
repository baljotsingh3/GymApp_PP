from django.core.paginator import Paginator
from django.shortcuts import render,redirect 
from django.views import View


from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from .mixins import *

from Member.models import * 
from Blog.models import *
from gymApp import *
from .forms import *


from Member.payment.gateways import PaymentGateway
from Member.signals import order_created

from Member.utils.llm import LLMService

#Authentication Views
class RegisterView(View):
    template_name = "Member/sign_up.html"

    def post(self, request):   
        form = MemberRegistrationForm(request.POST)
        if form.is_valid():
            print("form is valid")
            # Save User + Member (your custom form handles both)
            user = form.save()
            
            # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)  
            # first_name = models.CharField(max_length=50)
            # last_name = models.CharField(max_length=50)
            # phone_number = models.CharField(max_length=15)
            # email = models.EmailField(unique=True)
            # age = 
            Member.objects.create(
                user=user,
                first_name=form.cleaned_data.get('first_name'),
                last_name=form.cleaned_data.get('last_name'),
                email=user.email,
                age=form.cleaned_data.get('age'),
                # add other fields as needed
            )
            
            messages.success(request, "Registration successful!")
            # auto-login after registration (optional)
            login(request, user)
            return redirect("Member:login")
        else:
            print("Form errors:", form.errors)   # <
    
        return render(request, self.template_name, {"form": form})

    # GET request
    def get(self, request):                 
        form = MemberRegistrationForm()
        return render(request, self.template_name, {"form": form})
    

class LoginView(View):
    template_name = "Member/sign_in.html"

    def post(self, request):
        username = request.POST.get("gmail")  # ⚠️ maybe rename this to "email"
        password = request.POST.get("password")

        user = authenticate(request, email=username, password=password)
        print(user)
        if user is not None:
            login(request, user)
    
            #Redirect based on group
            if user.groups.filter(name="Trainer").exists():
                print("Trainer logged in")
                return redirect("Trainer:trainer_dashboard")  
            elif True: #user.groups.filter(name="Member").exists():
                print("Member logged in")
                return redirect("Member:member_dashboard")  
            else:
                messages.error(request, "You are not assigned to any group.")
                
                return redirect("Member:login")

        else:
            messages.error(request, "Invalid username or password.")
            return render(request, self.template_name)

    
    def get(self, request):
        return render(request, self.template_name)
  
  
#Dashboard View
class MemberDashboardView(LoginRequiredMixin, GroupRequiredMixin, View):
    
    template_name = "Member/dashboard.html" 
    login_url = "Member:login" 
    group_required = "Member" # must match exactly with the group name

    def get(self, request):
        context = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        context = {
            "username": request.user.username,
            "email": request.user.email,
        }
        return render(request, self.template_name, context)


class MemberProfileView(MemberDashboardView):
    template_name = "Member/profile.html"

    def get(self, request, *args, **kwargs):
        member = get_object_or_404(Member, user=request.user)

        blog = Blog.objects.filter(author=member.user)
        branches = GymBranch.objects.all()
        trainers = Trainer.objects.all()
        plans = Plan.objects.all()
        
        user_chats = CustomUser.objects.exclude(id=request.user.id).exclude(is_superuser=True)
        
        context = {
            "member": member,
            "branches": branches,
            "trainers": trainers,
            "plans": plans,
            
            "user_chats": user_chats,
            'blogs': blog,
        }
       
        
        return render(request, self.template_name, context)
    
    def post(self,request):

        try:
            member = request.user.member
        except Member.DoesNotExist:
            return redirect('Member:login')

        profile_picture= request.FILES.get("profile_picture")
        if profile_picture:
            member.profile_picture= profile_picture
            member.save()
            
        action = request.POST.get('action')

        if action == "update_profile":
            return self.update_profile(request, member)
        elif action == "custom_function":
            return self.custom_function(request, member)
        else:
            messages.error(request, "Unknown action")
            return redirect("Member:member_profile")



    def update_profile(self, request, member):
        try:
            member= member
        except Member.DoesNotExist:
            return redirect('Member:login')

        # Get form data
        member.first_name = request.POST.get("first_name", member.first_name)
        member.last_name = request.POST.get("last_name", member.last_name)
        member.phone_number = request.POST.get("phone_number", member.phone_number)
        member.email = request.POST.get("email", member.email)
        member.age = request.POST.get("age", member.age)

        branch_id = request.POST.get("branch")
        if branch_id:
            try:
                member.branch = GymBranch.objects.get(id=branch_id)
            except GymBranch.DoesNotExist:
                member.branch = None

        trainer_id = request.POST.get("assigned_trainer")
        if trainer_id:
            try:
                member.assigned_trainer = Trainer.objects.get(id=trainer_id)
            except Trainer.DoesNotExist:
                member.assigned_trainer = None

        plan_id = request.POST.get("plan")
        if plan_id:
            try:
                member.plan = Plan.objects.get(id=plan_id)
            except Plan.DoesNotExist:
                member.plan = None

        member.start_date = request.POST.get("start_date") or member.start_date
        member.height_cm = request.POST.get("height_cm") or member.height_cm
        member.weight_kg = request.POST.get("weight_kg") or member.weight_kg

        # Handle file upload
        profile_picture = request.FILES.get("profile_picture")
        if profile_picture:
            member.profile_picture = profile_picture

        member.save()

        # Handle other actions if needed
        return redirect('Member:member_profile')





class BillingHistory(MemberDashboardView):
    template_name = "Member/billing.html"
    
    def post(self, request):
        
        return render(request, self.template_name)
    
    
    def get(self, request):
        
        invoices = Invoice.objects.filter(payment__member__user=request.user).order_by('-generated_at')

        
        payment_history = Payment.objects.filter(member__user=request.user).order_by('-date')
    
        paginator = Paginator(payment_history, 7)  # show 5 payment_history per page
        page_number = request.GET.get('page')  # ?page=2
        page_obj = paginator.get_page(page_number)
        
        context = {
            "invoices": invoices,
            "payment_history": page_obj
        }
        return render(request, "Member/billing.html", context)



class PaymentForm(MemberDashboardView):
    
    template_name = "Member/Billing/payment_form.html"

    def post(self, request):
        amount = request.POST.get("amount")

        flag= False
        try:
            amount_paise = int(amount) * 100
            
            #razorpay creating order
            order = PaymentGateway()
            order_data = order.create_order(amount = amount_paise)
            
            
            # {'amount': 140000, 'amount_due': 140000, 
            #  'amount_paid': 0, 'attempts': 0, 
            #  'created_at': 1756635986, 
            #  'currency': 'INR', 'entity': 'order', 'id': 'order_RBuMrVRNPZAC2C', 'notes': [], 'offer_id': None, 'receipt': 'receipt_1', 'status': 'created'}
            
            #saving order details in database
            
            payment = order_created.send(sender=self.__class__, request= request, order=order_data)
        
            
        except (TypeError, ValueError):
            amount = None

        if payment:
            # Example: save payment
            # Payment.objects.create(user=request.user, amount=amount)
            messages.success(request, f"✅ Payment of Rs{amount} was successful!")
        else:
            messages.error(request, "❌ Please enter a valid amount.")

        return render(request, self.template_name)


    def get(self, request):
        
        return render(request, self.template_name)
    

class ChatBotView(MemberDashboardView):
    template_name = "Member/AI-chatbot/test_chat.html"
    
    def get(self, request):
        # Render the page initially with no response
        return render(request, self.template_name, {"response": ""})
