from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.translation import activate
from doctors.models import Doctor
from .serializers import DoctorSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.conf import settings
from collections import Counter

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Language code for translated fields (e.g., en, uz, ru)',
                required=True,
            ),
            OpenApiParameter(
                name='field',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Filter doctors by translated field (case-insensitive match)',
                required=False,
            ),
        ],
        description='Retrieve a list of doctors with translated fields in the specified language. '
                    'Optional filtering by translated `field`.'
    )
    def get(self, request, *args, **kwargs):
        lang_code = kwargs.get('lang_code')
        supported_languages = [lang['code'] for lang in settings.PARLER_LANGUAGES[None]]

        if lang_code not in supported_languages:
            return Response(
                {"error": f"Unsupported language code. Supported languages: {', '.join(supported_languages)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        activate(lang_code)

        # Handle query filtering
        field_query = request.query_params.get("field")
        queryset = self.get_queryset()

        if field_query:
            queryset = queryset.filter(translations__field__icontains=field_query)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DoctorFieldListView(generics.ListAPIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Language code for translated fields (e.g., en, uz, ru)',
                required=True,
            ),
        ],
        description='Retrieve a list of doctors filtered by medical field with translated fields in the specified language.'
    )
    def get(self, request, *args, **kwargs):
        lang_code = kwargs.get('lang_code')
        supported_languages = [lang['code'] for lang in settings.PARLER_LANGUAGES[None]]
        if lang_code not in supported_languages:
            return Response(
                {"error": f"Unsupported language code. Supported languages: {', '.join(supported_languages)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        activate(lang_code)
        doctors = Doctor.objects.all()
        fields_count = Counter(doctor.field for doctor in doctors)
        field_list = [{'field': field, 'count': count} for field, count in fields_count.items()]
        return Response(field_list)


class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='lang_code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.PATH,
                description='Language code for translated fields (e.g., en, uz, ru)',
                required=True,
            ),
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID of the doctor to retrieve',
                required=True,
            ),
        ],
        description='Retrieve details of a specific doctor with translated fields in the specified language.'
    )
    def get(self, request, *args, **kwargs):
        lang_code = kwargs.get('lang_code')
        supported_languages = [lang['code'] for lang in settings.PARLER_LANGUAGES[None]]
        if lang_code not in supported_languages:
            return Response(
                {"error": f"Unsupported language code. Supported languages: {', '.join(supported_languages)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        activate(lang_code)
        return super().get(request, *args, **kwargs)