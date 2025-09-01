from rest_framework import generics
from doctors.models import Hospital
from .serializers import HospitalSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from rest_framework.permissions import AllowAny


class HospitalListView(generics.ListAPIView):
    permission_classes = [AllowAny]
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

    @extend_schema(
        description='Retrieve a list of hospitals.'
    )
    def get(self, request, *args, **kwargs):
        # No translation needed for hospitals, but lang_code is in URL for consistency
        return super().get(request, *args, **kwargs)

class HospitalDetailView(generics.RetrieveAPIView):
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer
    permission_classes = [AllowAny]


    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the hospital to retrieve',
                required=True,
            ),
        ],
        description='Retrieve details of a specific hospital.'
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)