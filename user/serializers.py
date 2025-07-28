from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'help_text': 'Unique username for the user'},
            'email': {'help_text': 'User’s email address'},
            'password': {'help_text': 'User’s password (minimum 8 characters)'},
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='User’s email address')
    password = serializers.CharField(help_text='User’s password')

class VerifyCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='User’s email address')
    code = serializers.CharField(max_length=4, help_text='4-digit verification code sent to email')

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='User’s email address for password reset')

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(help_text='User’s email address')
    token = serializers.CharField(help_text='Password reset token')
    new_password = serializers.CharField(help_text='New password for the user')