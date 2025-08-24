from rest_framework import serializers
from booking.models import Booking
from datetime import datetime

class BookingSerializer(serializers.ModelSerializer):
    books = serializers.SerializerMethodField()
    number_of_pending = serializers.SerializerMethodField()
    number_of_approved = serializers.SerializerMethodField()
    number_of_rejected = serializers.SerializerMethodField()
    todays_appointments = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = ['id', 'user', 'doctor', 'appointment_date', 'status', 'books', 'number_of_pending', 'number_of_approved', 'number_of_rejected', 'todays_appointments']

    def get_books(self, obj):
        return Booking.objects.filter(doctor=obj.doctor).count()
    
    def get_todays_appointments(self, obj):
        today = datetime.now().date()
        return Booking.objects.filter(doctor=obj.doctor, appointment_date__date=today).count()
        
    def get_number_of_pending(self, obj):
        return Booking.objects.filter(doctor=obj.doctor, status='pending').count()
    def get_number_of_approved(self, obj):
        return Booking.objects.filter(doctor=obj.doctor, status='approved').count()
    def get_number_of_rejected(self, obj):
        return Booking.objects.filter(doctor=obj.doctor, status='rejected').count()

class StatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['status']

class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['doctor', 'appointment_date']

class FreeTimeSerializer(serializers.Serializer):
    free_times = serializers.DateField(required=True)

    class Meta:
        fields = ['free_times']