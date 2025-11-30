from rest_framework import serializers
from users.models import CustomUser
from doctors.models import Chat, Message

class UserInfoSerializer(serializers.ModelSerializer):
    last_chat_of_user = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'phone_number', 'last_chat_of_user']
    
    def get_last_chat_of_user(self, obj):
        try:
            chat = Chat.objects.filter(user_id_id=obj).latest('updated_at')
            all_messages = Message.objects.filter(chat=chat).order_by('-created_at')
            return MessageSerializer(all_messages, many=True).data
        except Chat.DoesNotExist:
            return None
        except Message.DoesNotExist:
            return None
        
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'is_from_user', 'content', 'file', 'image', 'voice', 'created_at']