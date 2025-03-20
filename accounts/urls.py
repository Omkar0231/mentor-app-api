from django.urls import path
<<<<<<< HEAD
from .views import RegisterView , LoginView 

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('signin/', LoginView.as_view(), name='signin'),  # 
=======
from .views import RegisterView , LoginView , VerifyOTPView , ResetPasswordView , VerifyResetOTPView , ForgotPasswordView

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path('signin/', LoginView.as_view(), name='signin'),  
    path('forgot-password/', ForgotPasswordView.as_view(), name='forgot-password'), 
    path('verify-reset-otp/', VerifyResetOTPView.as_view(), name='verify-reset-otp'), 
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'), 
>>>>>>> 416d1aa4160fb4fcbb31b4e1d4daf2204ab5dc11
]
