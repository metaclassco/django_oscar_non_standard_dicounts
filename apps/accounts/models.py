from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse_lazy


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    is_referral_code_used = models.BooleanField(default=False)
    bonuses = models.PositiveSmallIntegerField(default=0)
    referral_code = models.CharField(null=True, blank=True, max_length=10, unique=True)

    @property
    def referral_link(self):
        current_site = Site.objects.get_current()
        referral_url = reverse_lazy("offer:apply_referral_code", args=(self.referral_code,))
        return "http://%s%s" % (current_site.domain, referral_url)
