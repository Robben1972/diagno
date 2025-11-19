from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiExample
from .serializers import DoctorSerializer, DoctorSerializerCreate
from doctors.models import Doctor
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json

class MyDoctorsView(APIView):
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @extend_schema(
        summary="List all doctors for a clinic",
        description="Retrieve a list of doctors associated with the authenticated clinic user's hospital.",
        responses={
            200: DoctorSerializer(many=True),
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'clinic' role.")
        },
        tags=["Doctors"]
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated and user.role == 'clinic':
            doctors = Doctor.objects.filter(hospital__user=user)
            serializer = DoctorSerializer(doctors, many=True, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    

    @extend_schema(
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "image": {"type": "string", "format": "binary"},  # ✅ file
                    "data": {  # ✅ JSON body inside multipart
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "prize": {"type": "integer"},
                            "tags": {
                                "type": "array",
                                "items": {"type": "string"}
                            },
                            "field": {"type": "string"},
                            "fieldDescription": {"type": "string"},
                            "description": {"type": "string"},
                        },
                        "required": ["name", "translations"]
                    }
                },
            }
        },
        responses={201: DoctorSerializerCreate},
        examples=[
            OpenApiExample(
                "Doctor example",
                value={
                    "data": {
                        "name": "Dr. Ali",
                        "prize": 200000,
                        "tags": ["cardiologist", "surgeon"],
                        "field": "Kardiolog",
                        "fieldDescription": "Yurak kasalliklari mutaxassisi",
                        "description": "Yurak kasalliklari mutaxassisi"
                    },
                    "image": "(binary file)"
                },
            )
        ]
    )
    def post(self, request):
            user = request.user
            if not (user.is_authenticated and user.role == 'clinic'):
                return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            data = request.data.copy()

            # ✅ If wrapped inside "data"
            if "data" in data:
                try:
                    parsed = json.loads(data["data"])
                    data.pop("data")
                    data.update(parsed)
                except json.JSONDecodeError as e:
                    return Response({"error": f"Invalid JSON in 'data': {e}"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = DoctorSerializerCreate(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save(hospital=user.hospitals.first())
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MyDoctorDetailView(APIView):
    @extend_schema(
        summary="Retrieve a specific doctor's details",
        description="Retrieve details of a specific doctor associated with the authenticated clinic user's hospital.",
        responses={
            200: DoctorSerializer,
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'clinic' role."),
            404: OpenApiResponse(description="Doctor not found.")
        },
        tags=["Doctors"]
    )
    def get(self, request, pk):
        user = request.user
        if user.is_authenticated and user.role == 'clinic':
            try:
                doctor = Doctor.objects.get(pk=pk, hospital__user=user)
                serializer = DoctorSerializer(doctor, context={'request': request})
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        summary="Update a specific doctor's details",
        description="Update details of a specific doctor associated with the authenticated clinic user's hospital. Supports partial updates.",
        request=DoctorSerializer,
        responses={
            200: DoctorSerializer,
            400: OpenApiResponse(description="Bad request: Invalid data provided."),
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'clinic' role."),
            404: OpenApiResponse(description="Doctor not found.")
        },
        tags=["Doctors"]
    )
    def put(self, request, pk):
        user = request.user
        if user.is_authenticated and user.role == 'clinic':
            try:
                doctor = Doctor.objects.get(pk=pk, hospital__user=user)
                serializer = DoctorSerializer(doctor, data=request.data, partial=True, context={'request': request})
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

    @extend_schema(
        summary="Delete a specific doctor",
        description="Delete a specific doctor associated with the authenticated clinic user's hospital.",
        responses={
            204: OpenApiResponse(description="Doctor successfully deleted."),
            401: OpenApiResponse(description="Unauthorized: User is not authenticated or does not have the 'clinic' role."),
            404: OpenApiResponse(description="Doctor not found.")
        },
        tags=["Doctors"]
    )
    def delete(self, request, pk):
        user = request.user
        if user.is_authenticated and user.role == 'clinic':
            try:
                doctor = Doctor.objects.get(pk=pk, hospital__user=user)
                doctor.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Doctor.DoesNotExist:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)