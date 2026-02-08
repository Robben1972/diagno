from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .utils import generate_qr_png_bytes
from django.core.files.base import ContentFile

User = get_user_model()

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

        link = f"https://api.diagnoai.uz/{user.id}/"

        # ✅ generate QR and save to user.qrcode ImageField
        qr_bytes = generate_qr_png_bytes(link)
        user.qrcode.save(
            f"user_{user.id}_qr.png",
            ContentFile(qr_bytes),
            save=True
        )

        return user

class LoginSerializer(serializers.Serializer):
    email_or_phone = serializers.CharField()
    password = serializers.CharField(write_only=True)

# class UpdatePasswordSerializer(serializers.Serializer):
#     phone_number = serializers.CharField(max_length=15)
#     password = serializers.CharField(write_only=True, min_length=8)

#     def validate_phone_number(self, value):

#         try:
#             self.user = User.objects.get(phone_number=value)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("No user found with this phone number.")
#         return value

#     def validate_password(self, value):
#         try:
#             validate_password(value, self.user)
#         except ValidationError as e:
#             raise serializers.ValidationError(list(e.messages))
#         return value

#     def save(self):
#         new_password = self.validated_data['password']
#         self.user.set_password(new_password)
#         self.user.save()
#         return self.user
