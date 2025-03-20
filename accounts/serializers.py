from rest_framework import serializers
from django.contrib.auth.hashers import make_password
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

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)
