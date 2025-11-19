from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    last_name = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'password']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['phone_number'],
            # email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            first_name=validated_data['first_name'],
            last_name=validated_data.get('last_name', ''),  # 👈 safe get
            password=validated_data['password'],
            role='client'
        )
        return user

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
