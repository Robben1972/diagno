from rest_framework import serializers
from doctors.models import Chat, Message

class MessageSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    file = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'content', 'image', 'file', 'is_from_user', 'created_at', 'voice']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def get_file(self, obj):
        if obj.file:
            return obj.file.url
        return None

class ChatSerializer(serializers.ModelSerializer):
    message = serializers.CharField(required=False, write_only=True)
    latitude = serializers.FloatField(write_only=True, required=True)
    longitude = serializers.FloatField(write_only=True, required=True)
    user_id = serializers.CharField(required=False, write_only=True)  
    messages = MessageSerializer(many=True, read_only=True)

    # 👇 Add these
    image = serializers.ImageField(write_only=True, required=False, allow_null=True)
    file = serializers.FileField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Chat
        fields = [
            'id', 'user_id', 'created_at', 'updated_at',
            'message', 'image', 'file', 'latitude', 'longitude', 'messages'
        ]

    def create(self, validated_data):
        message_content = validated_data.pop('message', None)
        image = validated_data.pop('image', None)
        file = validated_data.pop('file', None)

        validated_data.pop('user_id', None)  # Not needed
        user = self.context['request'].user

        # Save chat
        chat = Chat.objects.create(user_id=user, **validated_data)

        # Save first message if provided
        if message_content or image or file:
            Message.objects.create(
                chat=chat,
                content=message_content,
                image=image,
                file=file,
                is_from_user=True
            )

        return chat
