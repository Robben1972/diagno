from deep_translator import GoogleTranslator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import activate
from .models import Doctor

from deep_translator import GoogleTranslator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import activate
from .models import Doctor


@receiver(post_save, sender=Doctor)
def create_translations(sender, instance, created, **kwargs):
    if getattr(instance, '_translations_updating', False):
        return

    if created:
        activate('uz')
        field = instance.safe_translation_getter('field', default='')
        fieldDescription = instance.safe_translation_getter('fieldDescription', default='')
        description = instance.safe_translation_getter('description', default='')

        if not instance.has_translation('ru'):
            instance.set_current_language('ru')
            instance.field = GoogleTranslator(source='uz', target='ru').translate(field) if field else ''
            instance.fieldDescription = GoogleTranslator(source='uz', target='ru').translate(fieldDescription) if fieldDescription else ''
            instance.description = GoogleTranslator(source='uz', target='ru').translate(description) if description else ''
            setattr(instance, '_translations_updating', True)
            try:
                instance.save()
            finally:
                setattr(instance, '_translations_updating', False)

        if not instance.has_translation('en'):
            instance.set_current_language('en')
            instance.field = GoogleTranslator(source='uz', target='en').translate(field) if field else ''
            instance.fieldDescription = GoogleTranslator(source='uz', target='en').translate(fieldDescription) if fieldDescription else ''
            instance.description = GoogleTranslator(source='uz', target='en').translate(description) if description else ''
            setattr(instance, '_translations_updating', True)
            try:
                instance.save()
            finally:
                setattr(instance, '_translations_updating', False)

    else:
        activate('uz')
        uz_field = instance.safe_translation_getter('field', default='')
        uz_fieldDescription = instance.safe_translation_getter('fieldDescription', default='')
        uz_description = instance.safe_translation_getter('description', default='')

        try:
            if instance.has_translation('ru'):
                instance.set_current_language('ru')
                new_field_ru = GoogleTranslator(source='uz', target='ru').translate(uz_field) if uz_field else ''
                new_fd_ru = GoogleTranslator(source='uz', target='ru').translate(uz_fieldDescription) if uz_fieldDescription else ''
                new_desc_ru = GoogleTranslator(source='uz', target='ru').translate(uz_description) if uz_description else ''

                changed = False
                if instance.field != new_field_ru:
                    instance.field = new_field_ru
                    changed = True
                if instance.fieldDescription != new_fd_ru:
                    instance.fieldDescription = new_fd_ru
                    changed = True
                if instance.description != new_desc_ru:
                    instance.description = new_desc_ru
                    changed = True

                if changed:
                    setattr(instance, '_translations_updating', True)
                    try:
                        instance.save()
                    finally:
                        setattr(instance, '_translations_updating', False)
            else:
                instance.set_current_language('ru')
                instance.field = GoogleTranslator(source='uz', target='ru').translate(uz_field) if uz_field else ''
                instance.fieldDescription = GoogleTranslator(source='uz', target='ru').translate(uz_fieldDescription) if uz_fieldDescription else ''
                instance.description = GoogleTranslator(source='uz', target='ru').translate(uz_description) if uz_description else ''
                setattr(instance, '_translations_updating', True)
                try:
                    instance.save()
                finally:
                    setattr(instance, '_translations_updating', False)
        except Exception:
            pass

        try:
            if instance.has_translation('en'):
                instance.set_current_language('en')
                new_field_en = GoogleTranslator(source='uz', target='en').translate(uz_field) if uz_field else ''
                new_fd_en = GoogleTranslator(source='uz', target='en').translate(uz_fieldDescription) if uz_fieldDescription else ''
                new_desc_en = GoogleTranslator(source='uz', target='en').translate(uz_description) if uz_description else ''

                changed = False
                if instance.field != new_field_en:
                    instance.field = new_field_en
                    changed = True
                if instance.fieldDescription != new_fd_en:
                    instance.fieldDescription = new_fd_en
                    changed = True
                if instance.description != new_desc_en:
                    instance.description = new_desc_en
                    changed = True

                if changed:
                    setattr(instance, '_translations_updating', True)
                    try:
                        instance.save()
                    finally:
                        setattr(instance, '_translations_updating', False)
            else:
                instance.set_current_language('en')
                instance.field = GoogleTranslator(source='uz', target='en').translate(uz_field) if uz_field else ''
                instance.fieldDescription = GoogleTranslator(source='uz', target='en').translate(uz_fieldDescription) if uz_fieldDescription else ''
                instance.description = GoogleTranslator(source='uz', target='en').translate(uz_description) if uz_description else ''
                setattr(instance, '_translations_updating', True)
                try:
                    instance.save()
                finally:
                    setattr(instance, '_translations_updating', False)
        except Exception:
            pass
