from django.urls import path
from .views import (
    HospitalListView, HospitalDetailView,
    DoctorListView, DoctorDetailView,
    ChatListView, ChatDetailView
)
urlpatterns = [
    path('hospitals/', HospitalListView.as_view(), name='hospital-list'),
    path('hospitals/<int:pk>/', HospitalDetailView.as_view(), name='hospital-detail'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('doctors/<int:pk>/', DoctorDetailView.as_view(), name='doctor-detail'),
    path('chats/', ChatListView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatDetailView.as_view(), name='chat-detail'),
]