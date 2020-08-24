from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.crypto import get_random_string

from .models import User


@receiver(pre_save, sender=User)
def generate_referral_code(instance, **kwargs):
    if not instance.referral_code:
        instance.referral_code = get_random_string(8)
