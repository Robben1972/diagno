from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from taggit_serializer.serializers import TagListSerializerField
from doctors.models import Doctor
from doctors.views.hospitals.serializers import HospitalSerializer


class DoctorTranslationSerializer(serializers.Serializer):
    field = serializers.CharField(max_length=100, default='')
    description = serializers.CharField(allow_blank=True, default='')


class DoctorSerializer(TranslatableModelSerializer):
    translations = TranslatedFieldsField(
        shared_model=Doctor,
        serializer_class=DoctorTranslationSerializer
    )
    hospital = HospitalSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        lang_code = self.context['request'].parser_context['kwargs'].get('lang_code', 'en')
        if 'translations' in ret:
            ret['translations'] = ret['translations'].get(lang_code, {})
        return ret

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'prize', 'image', 'tags', 'translations']
