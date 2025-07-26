from rest_framework import serializers
from .models import Hospital, Doctor, Chat, Message

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'latitude', 'longitude']

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'field', 'description']

class MessageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    file = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = Message
        fields = ['id', 'content', 'image', 'file', 'is_from_user', 'created_at']

class ChatSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False, allow_null=True, write_only=True)
    file = serializers.FileField(required=False, allow_null=True, write_only=True)
    message = serializers.CharField(required=False, write_only=True)
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    user_id = serializers.CharField(required=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = [
            'id', 'user_id', 'created_at', 'updated_at',
            'image', 'file', 'message', 'latitude', 'longitude', 'messages'
        ]

    def create(self, validated_data):
        message_content = validated_data.pop('message', None)
        image = validated_data.pop('image', None)
        file = validated_data.pop('file', None)
        
        chat = Chat.objects.create(**validated_data)
        
        if message_content or image or file:
            Message.objects.create(
                chat=chat,
                content=message_content,
                image=image,
                file=file,
                is_from_user=True
            )
        
        return chat