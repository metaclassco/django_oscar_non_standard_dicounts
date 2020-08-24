from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    is_referral_code_used = models.BooleanField(default=False)
    bonuses = models.PositiveSmallIntegerField(default=0)
