from django.db import models
from parler.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from django.conf import settings
from model_utils import FieldTracker

class Hospital(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hospitals')
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='hospital_images/', default='hospital_images/default_hospital.png')
    banner_image = models.ImageField(upload_to='hospital_images/', default='hospital_images/default_hospital.png')
    phone_number = models.CharField(max_length=20, blank=True)
    beds = models.IntegerField(default=0)
    description = models.TextField(blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

class Doctor(TranslatableModel):
    tracker = FieldTracker(fields=['name', 'prize', 'image'])
    translations = TranslatedFields(
        field=models.CharField(max_length=100, default=''),
        description=models.TextField(blank=True, default='')
    )
    name = models.CharField(max_length=255)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name='doctors')
    prize = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='doctor_images/', default='doctor_images/default_doctor.png')
    tags = TaggableManager(blank=True)

    def __str__(self):
        return f"{self.name} ({self.hospital.name})"

    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

class Chat(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"Chat {self.id} for User {self.user_id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='chat_images/', null=True, blank=True)
    file = models.FileField(upload_to='chat_files/', null=True, blank=True)
    is_from_user = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} in Chat {self.chat.id}"