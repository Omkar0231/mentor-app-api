from django.urls import path
from .views import RegisterView , LoginView , VerifyOTPView , ResetPasswordView , VerifyResetOTPView , ForgotPasswordView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signin/', LoginView.as_view(), name='signin'),  
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'), 
    path('verify-reset-otp/', VerifyResetOTPView.as_view(), name='verify-reset-otp'), 
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'), 
]
