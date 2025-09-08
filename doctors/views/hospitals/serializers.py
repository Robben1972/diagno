from rest_framework import serializers
from doctors.models import Hospital, Doctor

class HospitalSerializer(serializers.ModelSerializer):
    doctors = serializers.SerializerMethodField()
    departments = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_doctors(self, obj):
        doctors = Doctor.objects.filter(hospital=obj)
        return len(doctors)
    
    def get_departments(self, obj):
        doctors = Doctor.objects.filter(hospital=obj)
        return [doc.field for doc in doctors if doc.field]

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'image', 'phone_number', 'latitude', 'longitude', 'beds', 'doctors', 'description', 'departments']
