from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.dispatch import receiver
from django.db.models import signals


@receiver(signals.pre_save, sender=apps.get_model('project', 'ProjectIdea'))
def pre_save_license(sender, instance, **kwargs):
    if not instance.pk:
        instance.calculate_uniqueness()
    # else:
    #     try:
    #         old_instance = sender.objects.get(pk=instance.pk)
    #     except sender.DoesNotExist:
    #         pass
    #     else:
    #         if instance.report_content != old_instance.report_content:
    #             instance.calculate_uniqueness()

