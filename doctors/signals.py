from deep_translator import GoogleTranslator
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import activate
from .models import Doctor


@receiver(post_save, sender=Doctor)
def create_translations(sender, instance, created, **kwargs):
    if created:
        # get original uzbek values
        activate('uz')
        field = instance.safe_translation_getter('field', default='')
        description = instance.safe_translation_getter('description', default='')

        # Russian translation
        if not instance.has_translation('ru'):
            instance.set_current_language('ru')
            instance.field = GoogleTranslator(source='uz', target='ru').translate(field) if field else ''
            instance.description = GoogleTranslator(source='uz', target='ru').translate(description) if description else ''
            instance.save()

        # English translation
        if not instance.has_translation('en'):
            instance.set_current_language('en')
            instance.field = GoogleTranslator(source='uz', target='en').translate(field) if field else ''
            instance.description = GoogleTranslator(source='uz', target='en').translate(description) if description else ''
            instance.save()
