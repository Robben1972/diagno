from rest_framework import serializers
from parler_rest.serializers import TranslatableModelSerializer, TranslatedFieldsField
from taggit_serializer.serializers import TagListSerializerField
from doctors.models import Doctor
from doctors.views.hospitals.serializers import HospitalSerializer
from parler.utils.context import switch_language
from deep_translator import GoogleTranslator


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
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        lang_code = self.context['request'].parser_context['kwargs'].get('lang_code', 'en')
        if 'translations' in ret:
            ret['translations'] = ret['translations'].get(lang_code, {})
        return ret

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'prize', 'image','tags', 'translations']

class DoctorSerializerCreate(TranslatableModelSerializer):
    field = serializers.CharField(required=False, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    image = serializers.SerializerMethodField()

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

    hospital = HospitalSerializer(read_only=True)
    tags = TagListSerializerField(required=False)

    class Meta:
        model = Doctor
        fields = ['id', 'name', 'hospital', 'prize', 'image', 'tags',
                  'field', 'description']

    def create(self, validated_data):
        field = validated_data.pop("field", "")
        description = validated_data.pop("description", "")

        doctor = Doctor.objects.create(**validated_data)

        # ✅ Save Uzbek translation by default
        with switch_language(doctor, "uz"):
            doctor.field = field
            doctor.description = description
            doctor.save()
        
        # ✅ Generate RU translation
        with switch_language(doctor, "ru"):
                doctor.field = GoogleTranslator(source="uz", target="ru").translate(field) if field else ""
                doctor.description = GoogleTranslator(source="uz", target="ru").translate(description) if description else ""
                doctor.save()

        # ✅ Generate EN translation
        with switch_language(doctor, "en"):
                doctor.field = GoogleTranslator(source="uz", target="en").translate(field) if field else ""
                doctor.description = GoogleTranslator(source="uz", target="en").translate(description) if description else ""
                doctor.save()

        return doctor

    def to_representation(self, instance):
        # ✅ Always show Uzbek by default
        with switch_language(instance, "uz"):
            ret = super().to_representation(instance)
            ret["field"] = instance.field
            ret["description"] = instance.description
        return ret