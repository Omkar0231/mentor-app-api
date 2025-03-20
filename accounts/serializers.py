from rest_framework import serializers
from django.contrib.auth.hashers import make_password
<<<<<<< HEAD
from django.contrib.auth import authenticate
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True)
    role = serializers.CharField(required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ['role', 'first_name', 'last_name', 'email', 'phone_number' , 'password', 'confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before saving
        validated_data['password'] = make_password(validated_data['password'])  # Hash password
        return CustomUser.objects.create(**validated_data)

=======
from .models import CustomUser, OTPVerification
from rest_framework import serializers
from django.core.mail import send_mail
import random
from .models import CustomUser  # Import your user model
from datetime import timedelta
from django.utils.timezone import now

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Create user
        user = CustomUser.objects.create_user(**validated_data)

        # Generate OTP
        otp = str(random.randint(100000, 999999))
        user.otp = otp  # Store OTP in the user model
        user.save()

        # Send OTP email
        send_mail(
            subject='Your OTP Code',
            message=f'Your OTP is: {otp}',
            from_email='your_email@gmail.com',  # Use your email
            recipient_list=[user.email],
            fail_silently=False
        )

        return user



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)

    def validate(self, data):
        try:
            otp_record = OTPVerification.objects.get(email=data['email'])
            
            # OPTIONAL: Check if OTP is expired (e.g., 5 minutes expiry)
            if otp_record.created_at < now() - timedelta(minutes=5):
                raise serializers.ValidationError("OTP has expired")

            if otp_record.otp != data['otp']:
                raise serializers.ValidationError("Invalid OTP")

        except OTPVerification.DoesNotExist:
            raise serializers.ValidationError("OTP not found")

        return data
>>>>>>> 416d1aa4160fb4fcbb31b4e1d4daf2204ab5dc11

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
<<<<<<< HEAD

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError("Email and password are required.")

        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")

        data['user'] = user
        return data
=======
>>>>>>> 416d1aa4160fb4fcbb31b4e1d4daf2204ab5dc11
