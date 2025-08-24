from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from booking.models import Booking
from django.utils.dateparse import parse_date
from booking.serializers import BookingSerializer, StatusUpdateSerializer, CreateBookingSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from booking.service.send_mail import send_booking_status

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes

from datetime import date


class DoctorBookingView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter bookings by status (e.g., pending, confirmed, cancelled)",
                required=False,
            ),
            OpenApiParameter(
                name="today",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="If true, return only today's bookings (appointment_date = today)",
                required=False,
            ),
        ],
        description="Retrieve all bookings for doctors of the authenticated clinic user. "
                    "Optionally filter by status or restrict to today's bookings."
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'clinic':
            bookings = Booking.objects.filter(doctor__hospital__user=user)

            # Filter by status
            status_param = request.query_params.get("status")
            if status_param:
                bookings = bookings.filter(status=status_param)

            # Filter by today
            today_param = request.query_params.get("today")
            if today_param and today_param.lower() in ["true", "1", "yes"]:
                bookings = bookings.filter(appointment_date__date=date.today())

            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


class UserBookingsView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="status",
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description="Filter bookings by status (e.g., pending, confirmed, cancelled)",
                required=False,
            ),
            OpenApiParameter(
                name="today",
                type=OpenApiTypes.BOOL,
                location=OpenApiParameter.QUERY,
                description="If true, return only today's bookings (appointment_date = today)",
                required=False,
            ),
        ],
        description="Retrieve all bookings for the authenticated client user. "
                    "Optionally filter by status or restrict to today's bookings."
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            bookings = Booking.objects.filter(user=user)

            # Filter by status
            status_param = request.query_params.get("status")
            if status_param:
                bookings = bookings.filter(status=status_param)

            # Filter by today
            today_param = request.query_params.get("today")
            if today_param and today_param.lower() in ["true", "1", "yes"]:
                bookings = bookings.filter(appointment_date__date=date.today())

            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class CreateBookingView(APIView):
    @extend_schema(
        summary="Create a new booking",
        description="Create a new booking for an authenticated client user.",
        request=CreateBookingSerializer,
        responses={
            201: BookingSerializer,
            400: OpenApiResponse(description="Bad request: Invalid data provided."),
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'client' role.")
        },
        tags=["Bookings"]
    )
    def post(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'client':
            serializer = CreateBookingSerializer(data=request.data)
            if serializer.is_valid():
                booking = serializer.save(user=user)
                return Response(BookingSerializer(booking).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

class UpdateBookingView(APIView):
    @extend_schema(
        summary="Update booking status",
        description="Update the status of a specific booking. Only clinic users associated with the booking's doctor can update the status.",
        request=StatusUpdateSerializer,
        responses={
            200: StatusUpdateSerializer,
            400: OpenApiResponse(description="Bad request: Invalid data provided."),
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'clinic' role."),
            404: OpenApiResponse(description="Booking not found.")
        },
        tags=["Bookings"]
    )
    def put(self, request, lang_code, booking_id):
        user = request.user
        try:
            booking = Booking.objects.get(id=booking_id)
            if user.is_authenticated and (user.role == 'clinic' and booking.doctor.hospital.user == user):
                serializer = StatusUpdateSerializer(booking, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    send_booking_status(booking.user.email, booking.appointment_date.date().isoformat(), booking.appointment_date.time().isoformat(), booking.doctor.name, lang_code, request.data['status'])
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, lang_code, booking_id):
        user = request.user
        try:
            booking = Booking.objects.get(id=booking_id)
            if user.is_authenticated and (user.role == 'client' and booking.user == user):
                booking.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except Booking.DoesNotExist:
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        

class DoktorFreeTimeView(APIView):
    @extend_schema(
        summary="Get booked times for a doctor",
        description="Retrieve all booked appointment times for a given doctor on a specific date. Only clients can access this endpoint.",
        parameters=[
            OpenApiParameter(
                name="date",
                description="Date in ISO format (YYYY-MM-DD) for which to check booked times",
                required=True,
                type=str,
                location=OpenApiParameter.QUERY,
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=dict,
                description="Booked times returned successfully",
                examples=[
                    OpenApiExample(
                        "Booked times example",
                        value={
                            "booked_times": [
                                "09:00:00",
                                "10:30:00"
                            ]
                        },
                    )
                ],
            ),
            401: OpenApiResponse(
                description="Unauthorized – only authenticated clients can access this endpoint",
                response=dict,
            ),
            400: OpenApiResponse(
                description="Bad Request – date is missing or invalid",
                response=dict,
            ),
        },
    )
    def get(self, request, doctor_id):
        user = request.user
        date_str = request.query_params.get("date")

        if not date_str:
            return Response({"error": "date query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not user.is_authenticated or user.role != "client":
            return Response({"error": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

        parsed_date = parse_date(date_str)
        if not parsed_date:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(
            doctor_id=doctor_id,
            status__in=["pending", "confirmed"],
            appointment_date__date=parsed_date,
        ).values_list("appointment_date", flat=True)

        booked_times = [dt.time().isoformat() for dt in bookings]

        return Response({"booked_times": booked_times}, status=status.HTTP_200_OK)