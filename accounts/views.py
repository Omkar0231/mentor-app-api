from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, authenticate
from knox.models import AuthToken
from .models import CustomUser, OTPVerification
from .serializers import  VerifyOTPSerializer, LoginSerializer
from django.contrib.auth.hashers import make_password , check_password
from django.core.mail import send_mail
import random
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated



class RegisterView(APIView):
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = send_otp_email(email)  # Generate and send OTP

        # Save OTP in the OTPVerification model
        OTPVerification.objects.update_or_create(
            email=email,
            defaults={'otp': otp , 'password': make_password(password), 'created_at': now()}
        )

        return Response({'message': 'OTP sent to email'}, status=status.HTTP_200_OK)

def send_otp_email(email):
    otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
    subject = 'Your OTP Code'
    message = f'Your OTP code is: {otp}'
    from_email = 'your_email@gmail.com'  # Use the same email from settings.py
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return otp  # Store and verify later

class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            try:
                otp_record = OTPVerification.objects.get(email=request.data['email'])

                if CustomUser.objects.filter(email=otp_record.email).exists():
                    return Response({"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST)

                # ✅ Get stored password (already hashed)
                stored_password = otp_record.password
                # stored_first_name = otp_record.first_name
                # stored_last_name = otp_record.last_name
                print("Stored Hashed Password:", stored_password)
                if not stored_password:
                    return Response({"error": "Something went wrong, please register again"}, status=status.HTTP_400_BAD_REQUEST)

                # ✅ Create user with the stored password
                user = CustomUser(email=otp_record.email, password=stored_password)
                #, first_name=stored_first_name , last_name=stored_last_name
                user.save()

                otp_record.delete()  # Cleanup OTP record
                return Response({"message": "Account verified successfully"}, status=status.HTTP_201_CREATED)

            except OTPVerification.DoesNotExist:
                return Response({"error": "Invalid OTP or email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        print("Received Data:", request.data)  
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            print("Serializer Errors:", serializer.errors) 
            print("Validated Data:", serializer.validated_data)  # Debugging line
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            
            try:
                user = User.objects.get(email=email)  # Get user by email
                print("User Exists:", user.email, user.password) 

                   # 🔥 Debug password check 🔥
                print("user Password:", user.password)
                
                password_check =  check_password(password , user.password)
                print("Password:", password)
                print("Password Matches:", password_check)
                
                if password_check:  # Check hashed password
                    _, token = AuthToken.objects.create(user)
                    return Response({"message": "Login successful", "token": token}, status=status.HTTP_200_OK)
                
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
            
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        print("Email:", email)
        if not email:
            return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
            OTPVerification.objects.update_or_create(email=email, defaults={"otp": otp, "created_at": now()})

            # Send OTP via Email
            send_mail(
                "Reset Your Password",
                f"Your OTP for password reset is: {otp}",
                "your_email@gmail.com",  # Replace with actual sender email
                [email],
            )

            return Response({"message": "OTP sent to email"}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class VerifyResetOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        if not email or not otp:
            return Response({"error": "Email and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTPVerification.objects.get(email=email, otp=otp)
            return Response({"message": "OTP verified successfully"}, status=status.HTTP_200_OK)
        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        if not email or not otp or not new_password:
            return Response({"error": "Email, OTP, and New Password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            otp_record = OTPVerification.objects.get(email=email, otp=otp)
            user = CustomUser.objects.get(email=email)
            user.set_password(new_password)  # Hash the password
            user.save()

            otp_record.delete()  # Delete OTP after successful password reset
            return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)

        except OTPVerification.DoesNotExist:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class UpdatePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # ✅ User must be logged in

    def post(self, request):
        user = request.user  # ✅ Get the logged-in user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        # ✅ Check if both fields are provided
        if not current_password or not new_password:
            return Response({"error": "Current password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Check if current password is correct
        if not check_password(current_password, user.password):
            return Response({"error": "Incorrect current password"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ Hash and update new password securely
        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

