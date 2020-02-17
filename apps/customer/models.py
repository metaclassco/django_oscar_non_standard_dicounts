from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    birthday = models.DateField(null=True)
    is_affiliate_discount_used = models.BooleanField(default=False)
    bonuses = models.PositiveSmallIntegerField(default=0)


from oscar.apps.customer.models import *  # noqa isort:skip
