from rest_framework import serializers
from .models import Hospital, Doctor, Chat

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'latitude', 'longitude']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'field', 'description']

class ChatSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)
    message = serializers.CharField(required=False, write_only=True)
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    user_id = serializers.CharField(required=True)

    class Meta:
        model = Chat
        fields = [
            'id', 'user_id', 'history', 'created_at', 'updated_at',
            'image', 'file', 'message', 'latitude', 'longitude'
        ]

    def create(self, validated_data):
        # Only pop fields not in the model
        validated_data.pop('message', None)
        validated_data.pop('title', None)
        # Do NOT pop latitude and longitude
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('message', None)
        validated_data.pop('title', None)
        # Do NOT pop latitude and longitude
        return super().update(instance, validated_data)
