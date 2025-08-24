from django.contrib import admin
from .models import Hospital, Doctor, Chat, Message
from parler.admin import TranslatableAdmin


# Register your models here.
admin.site.register(Hospital)
@admin.register(Doctor)
class DoctorAdmin(TranslatableAdmin):
    pass

admin.site.register(Chat)
admin.site.register(Message)
