from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import EmailUser


@receiver(pre_save, sender=EmailUser)
def is_active_handler(sender, instance, **kwargs):
    old = EmailUser.objects.filter(id=instance.id).first()
    if old and (
            old.death != instance.death or old.retired != instance.retired):
        instance.is_active = False
