
from GymApi.authentication.tokens import TokenGenerator
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .permissions import *
from rest_framework import status

from gymApp.models import *
from Member.models import *
from Trainer.models import *

from rest_framework.permissions import AllowAny

from .serializers import *


from rest_framework.decorators import action
from rest_framework.reverse import reverse



class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    

    def get_permissions(self):
        """
        Custom permission logic:
        - list & retrieve are public (anyone can see trainers)
        - create, update, delete require authenticated Trainer
        """
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]  # public access
        else:
            permission_classes = [IsAuthenticated, IsTrainer]  # restricted
        return [perm() for perm in permission_classes]

    
    # GET /trainers/  -> list all trainers
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        
        data = [
            {
                "name": f"{trainer.first_name} {trainer.last_name}",
                "detail": reverse("trainers-detail", args=[trainer.pk], request=request)
            }
            
            for trainer in queryset
        ]

        return Response({
            "count": queryset.count(),
            "results": data
        }, status=status.HTTP_200_OK)
        
        
    # GET /trainers/{pk}/  -> retrieve one trainer
    def retrieve(self, request, *args, **kwargs):
        trainer = self.get_object()
        serializer = self.get_serializer(trainer)
        return Response(serializer.data, status=status.HTTP_200_OK)


    #make trainer
    def create(self, request, *args, **kwargs):
        user_data = request.data.get("user")  # expecting nested CustomUser data
        trainer_data = request.data.copy()

        if not user_data:
            return Response(
                {"error": "User details required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Create CustomUser
        user = CustomUser.objects.create_user(
            username=user_data.get("username"),
            email=user_data.get("email"),
            password=user_data.get("password"),
            first_name=user_data.get("first_name", ""),
            last_name=user_data.get("last_name", "")
        )

        # 2. Assign user to "Trainer" group
        group, _ = Group.objects.get_or_create(name="Trainer")
        user.groups.add(group)

        # 3. Create Trainer profile (OneToOne with CustomUser)
        trainer_data["User"] = user.id  # since OneToOne field expects user pk
        serializer = self.get_serializer(data=trainer_data)
        serializer.is_valid(raise_exception=True)
        trainer = serializer.save(User=user)

        return Response(
            self.get_serializer(trainer).data,
            status=status.HTTP_201_CREATED
        )
        
        
    # PATCH /trainers/{pk}/  -> partial update
    def partial_update(self, request, *args, **kwargs):
        trainer = self.get_object()
        serializer = self.get_serializer(trainer, data=request.data, partial=True)
        if serializer.is_valid():
            trainer = serializer.save()
            return Response(self.get_serializer(trainer).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE /trainers/{pk}/  -> delete trainer
    def destroy(self, request, *args, **kwargs):
        trainer = self.get_object()
        trainer.delete()
        return Response({"message": "Trainer deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    # Custom action -> GET /trainers/by-name/{name}/
    @action(detail=False, methods=["get"], url_path="by-name/(?P<name>[^/.]+)")
    def get_by_name(self, request, name=None):
        trainers = Trainer.objects.filter(first_name__iexact=name)
        if not trainers.exists():
            return Response({"error": "Trainer not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(trainers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




#User management Authentication
class TrainerRegisterView(APIView):
    permission_classes = [AllowAny] 
    
    def post(self, request):
        
        print("inside trainer register view")
        serializer = TrainerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
           
            return Response(
                {"message": "Trainer registered successfully!", "username": user.first_name },
                status=status.HTTP_201_CREATED
            )
            
        return Response({"errors": serializer.errors} , status=status.HTTP_400_BAD_REQUEST)
          


class GenerateAndSendTokenView(APIView):

  # Only logged-in users can call

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"error": "email and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(email=email, password=password)
        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # gene
        token= TokenGenerator()
        key= token.send_token_email(user)

        return Response(
            {"message": f"Token has been sent to {user.email}"},
            status=status.HTTP_200_OK
        )
        


# Members

# class MemberViewSet(viewsets.ModelViewSet):
    # queryset = Member.objects.all()
    # serializer_class = MemberSerializer
    #   # tweak if some endpoints should be public

    # def get_permissions(self):
    #     """
    #     Custom permission logic:
    #     - list & retrieve are public (anyone can see trainers)
    #     - create, update, delete require authenticated Trainer
    #     """
    #     if self.action in ["list"]:
    #         permission_classes = [permissions.AllowAny]  # public access
    #     elif self.action in ["destroy", "update"]:
    #         permission_classes = [IsMember]
    #     else:
    #         permission_classes= [IsTrainer]# restricted
    #     return [perm() for perm in permission_classes]


    # # CREATE a new member
    # def create(self, request, *args, **kwargs):
    #     user_data = request.data.get("user")  # expecting nested user details
    #     member_data = request.data.copy()

    #     if not user_data:
    #         return Response(
    #             {"error": "User details required"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # 1. Create CustomUser
    #     user = CustomUser.objects.create_user(
    #         username=user_data.get("username"),
    #         email=user_data.get("email"),
    #         password=user_data.get("password"),
    #         first_name=user_data.get("first_name", ""),
    #         last_name=user_data.get("last_name", "")
    #     )

    #     # 2. Attach user to member
    #     member_data["user"] = user.id
    #     serializer = self.get_serializer(data=member_data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)

    #     return Response(serializer.data, status=status.HTTP_201_CREATED)


    # # LIST all members
    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     data = [
    #         {
    #             "name": f"{member.first_name} {member.last_name}",
    #             "email": member.email,
    #             "detail": request.build_absolute_uri(f"/api/members/{member.pk}/")
    #         }
    #         for member in queryset
    #     ]
    #     return Response({
    #         "count": queryset.count(),
    #         "results": data
    #     }, status=status.HTTP_200_OK)

    # # RETRIEVE one member
    # def retrieve(self, request, *args, **kwargs):
    #     member = self.get_object()
    #     serializer = self.get_serializer(member)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    # # UPDATE (PATCH / PUT)
    # def update(self, request, *args, **kwargs):
    #     member = self.get_object()
    #     serializer = self.get_serializer(member, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


    # # DELETE
    # def destroy(self, request, *args, **kwargs):
    #     member = self.get_object()
    #     member.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
        # GET /invoices/ -> list all invoices
    
    def get_permissions(self):
        """
        Custom permission logic:
        - list & retrieve are public (anyone can see trainers)
        - create, update, delete require authenticated Trainer
        """
        if self.action in ["list"]:
            permission_classes = [permissions.AllowAny]  # public access
        elif self.action in ["retrieve"]:
            permission_classes = [ IsTrainerOrMember]  # restricted
        else:
            permission_classes= [IsTrainer]
        return [perm() for perm in permission_classes]

    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "count": queryset.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)
     
        
    lookup_field = "username"   # instead of pk

    def retrieve(self, request, username=None, *args, **kwargs):
        """
        GET /invoices/{username}/  -> fetch all invoices for given username
        """
        invoices = self.get_queryset().filter(payment__member__user__username=username)

        if not invoices.exists():
            return Response(
                {"error": f"No invoices found for username '{username}'"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(invoices, many=True)
        return Response({
            "count": invoices.count(),
            "results": serializer.data
        }, status=status.HTTP_200_OK)

    
# class PaymentViewSet(viewsets.ModelViewSet):
#     queryset = Payment.objects.all()
#     serializer_class = PaymentSerializer

#     def create(self, request, *args, **kwargs):
#         """
#         Create a new Payment entry for a member.
#         - Generate order_id automatically
#         - Require member_id, amount, and optionally plan_id
#         """

#         member_id = request.data.get("member_id")
#         plan_id = request.data.get("plan_id")
#         amount = request.data.get("amount")

#         if not member_id or not amount:
#             return Response(
#                 {"error": "member_id and amount are required"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         member = get_object_or_404(Member, pk=member_id)
#         plan = None
#         if plan_id:
#             plan = get_object_or_404(Plan, pk=plan_id)

#         # Generate unique order_id
#         order_id = f"ORD-{uuid.uuid4().hex[:10].upper()}"

#         payment = Payment.objects.create(
#             member=member,
#             plan=plan,
#             order_id=order_id,
#             amount=amount,
#             status="created",  # default
#         )

#         serializer = self.get_serializer(payment)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)