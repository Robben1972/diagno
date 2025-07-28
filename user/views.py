from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import (
    UserRegistrationSerializer,
    LoginSerializer,
    VerifyCodeSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
)
from .models import User
from django.core.cache import cache
from django.core.mail import send_mail
import random
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.crypto import get_random_string
from django.conf import settings
from rest_framework.permissions import AllowAny

class RegisterView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=UserRegistrationSerializer,
        responses={
            201: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'refresh': {'type': 'string'},
                        'access': {'type': 'string'},
                    },
                },
                description='User registered successfully, returns JWT tokens',
            ),
            400: OpenApiResponse(description='Invalid input data'),
        },
        description='Register a new user and return JWT tokens',
    )
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=LoginSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'},
                    },
                },
                description='Verification code sent to email',
            ),
            401: OpenApiResponse(description='Invalid credentials'),
            400: OpenApiResponse(description='Invalid input data'),
        },
        description='Initiate login by sending a verification code to the user’s email',
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    code = str(random.randint(1000, 9999))
                    cache.set(f"login_code_{email}", code, timeout=60)
                    
                    send_mail(
                        'Your Login Code',
                        f'Your verification code is: {code}',
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    return Response({
                        'message': 'Verification code sent to email'
                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyCodeView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=VerifyCodeSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'refresh': {'type': 'string'},
                        'access': {'type': 'string'},
                    },
                },
                description='Verification successful, returns JWT tokens',
            ),
            400: OpenApiResponse(description='Invalid or expired code'),
        },
        description='Verify the login code sent to the user’s email and return JWT tokens',
    )
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            code = serializer.validated_data['code']
            
            cached_code = cache.get(f"login_code_{email}")
            if cached_code and cached_code == code:
                user = User.objects.get(email=email)
                refresh = RefreshToken.for_user(user)
                cache.delete(f"login_code_{email}")
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid or expired code'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=PasswordResetRequestSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'},
                    },
                },
                description='Password reset link sent to email',
            ),
            404: OpenApiResponse(description='Email not found'),
            400: OpenApiResponse(description='Invalid input data'),
        },
        description='Request a password reset link to be sent to the user’s email',
    )
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                token = get_random_string(length=32)
                cache.set(f"reset_token_{email}", token, timeout=3600)
                
                reset_link = f"http://localhost:8000/reset-password/?email={email}&token={token}"
                send_mail(
                    'Password Reset Request',
                    f'Click this link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                return Response({'message': 'Password reset link sent'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request=PasswordResetConfirmSerializer,
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'message': {'type': 'string'},
                    },
                },
                description='Password reset successful',
            ),
            400: OpenApiResponse(description='Invalid or expired token'),
            404: OpenApiResponse(description='User not found'),
        },
        description='Confirm password reset with token and set new password',
    )
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            cached_token = cache.get(f"reset_token_{email}")
            if cached_token and cached_token == token:
                try:
                    user = User.objects.get(email=email)
                    user.set_password(new_password)
                    user.save()
                    cache.delete(f"reset_token_{email}")
                    return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
                except User.DoesNotExist:
                    return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(APIView):
    permission_classes = (AllowAny,)

    @extend_schema(
        request={
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string'},
            },
            'required': ['refresh'],
        },
        responses={
            200: OpenApiResponse(
                response={
                    'type': 'object',
                    'properties': {
                        'access': {'type': 'string'},
                    },
                },
                description='New access token generated',
            ),
            400: OpenApiResponse(description='Invalid or missing refresh token'),
        },
        description='Refresh JWT access token using a valid refresh token',
    )
    def post(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({'access': access_token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)