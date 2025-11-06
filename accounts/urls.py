from django.urls import path
from .views import SignupView, LoginView, LogoutView, PasswordResetRequestView, CodeVerifyView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('verify-code/', CodeVerifyView.as_view(), name='verify_code'),
]