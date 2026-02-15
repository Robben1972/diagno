from django.urls import path
from doctors.views.chat.views import (ChatListView, ChatDetailView, CreateChatWithDoctorView)
from doctors.views.doctors.views import DoctorListView, DoctorDetailView, DoctorFieldListView
from doctors.views.hospitals.views import HospitalListView, HospitalDetailView
from doctors.views.clinic.views import MyDoctorsView, MyDoctorDetailView

urlpatterns = [
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
    path('chats/doctor/<int:doctor_id>/', CreateChatWithDoctorView.as_view(), name='create-chat-with-doctor'),

    path('api/<str:lang_code>/doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('api/<str:lang_code>/doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('api/<str:lang_code>/doctors/field/', DoctorFieldListView.as_view(), name='doctor-field-list'),
    path('api/hospitals/', HospitalListView.as_view(), name='hospital-list'),
    path('api/hospitals/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),

    path('api/my-doctors/', MyDoctorsView.as_view(), name='my-doctor-list'), 
    path('api/my-doctors/<int:pk>/', MyDoctorDetailView.as_view(), name='my-doctor-detail'),
]
