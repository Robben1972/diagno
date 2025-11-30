from django.urls import path
from .views import DoctorBookingView, UserBookingsView, CreateBookingView, UpdateBookingView, DoktorFreeTimeView
from .view.userInfo.views import UserInfoView

urlpatterns = [
    path('doctor/bookings/', DoctorBookingView.as_view(), name='doctor-bookings'),
    path('user/bookings/', UserBookingsView.as_view(), name='user-bookings'),
    path('bookings/create/', CreateBookingView.as_view(), name='create-booking'),
    path('bookings/<str:lang_code>/<int:booking_id>/update/', UpdateBookingView.as_view(), name='update-booking'),
    path('doctors/<int:doctor_id>/free-times/', DoktorFreeTimeView.as_view(), name='doctor-free-times'),
    path('user/<int:user_id>/info/', UserInfoView.as_view(), name='user-info'),
]