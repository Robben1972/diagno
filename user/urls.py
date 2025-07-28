from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    VerifyCodeView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
    TokenRefreshView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify_code'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]