from django.db.models.signals import post_save
from django.dispatch import receiver

from user.models import User
from .models import Code


@receiver(post_save, sender=User)
def post_save_generate_code(sender, instance, created, *args, **kwargs):
    if created:
        Code.objects.create(user=instance)
