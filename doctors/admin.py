from django.contrib import admin
from .models import Hospital, Doctor, Chat, Message

# Register your models here.
admin.site.register(Hospital)
admin.site.register(Doctor)
admin.site.register(Chat)
admin.site.register(Message)
