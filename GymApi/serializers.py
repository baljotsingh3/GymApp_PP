from rest_framework import serializers

from gymApp.models import *
from Member.models import *
from Trainer.models import *    
from django.contrib.auth.models import Group


class TrainerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trainer
        fields = '__all__'



class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'



# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
    
#     class Meta:
#         model= CustomUser
#         fields= ('username', 'email', 'password')
        
#     def create(self, validated_data):
        
#         user = CustomUser.objects.create_user(
#             username=validated_data["username"],
#             email=validated_data.get("email"),
#             password=validated_data["password"]
#         )
        
#          # assign user to "member" group
#         try:
#             group = Group.objects.get(name="Member")
            
#         except Group.DoesNotExist:
#             group = Group.objects.create(name="Member")
            
#         user.groups.add(group)
        
         
#         return user


class TrainerRegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    specialization = serializers.CharField()
    experience_years = serializers.IntegerField()

    class Meta:
        model = CustomUser
        fields = [
            "username", "email", "password",
            "first_name", "last_name", "phone_number",
            "specialization", "experience_years"
        ]

    def create(self, validated_data):
        # Extract user data
        try:
            
            username = validated_data.pop("username")
            email = validated_data.pop("email")
            password = validated_data.pop("password")

            # Create CustomUser
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            # Assign user to Trainer group
            group, created = Group.objects.get_or_create(name="Trainer")
            user.groups.add(group)

            
            print("Validated Data:", validated_data)
            
            
            # Create Trainer instance
            print("Trainer record created")
            
            trainer = Trainer.objects.create(
                User=user,
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email=email,
                phone_number=validated_data["phone_number"],
                specialization=validated_data["specialization"],
                experience_years=validated_data["experience_years"]
            )
            print("Trainer saved")

            return trainer
        except Exception as e:
            print("Error in TrainerRegisterSerializer:", e)
            raise serializers.ValidationError({"error": str(e)})



class PaymentSerializer(serializers.ModelSerializer):
    member_name = serializers.CharField(source="member.user.username", read_only=True)

    class Meta:
        model = Payment
        fields = ["id", "order_id", "payment_id", "amount", "currency", "status", "date", "member_name"]


class InvoiceSerializer(serializers.ModelSerializer):
    payment = PaymentSerializer(read_only=True)  # Nested serializer
    payment_id = serializers.PrimaryKeyRelatedField(
        queryset=Payment.objects.all(),
        source="payment",
        write_only=True
    )

    class Meta:
        model = Invoice
        fields = ["id", "payment", "payment_id", "pdf_file", "generated_at"]