from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site
from django.db import models
from django.urls import reverse_lazy


class User(AbstractUser):
    date_of_birth = models.DateField(null=True)
    is_referral_code_used = models.BooleanField(default=False)
    referral_code = models.CharField(null=True, blank=True, max_length=10, unique=True)
    referrer = models.ForeignKey('User', null=True, blank=True, related_name='referees', on_delete=models.SET_NULL)

    @property
    def referral_link(self):
        current_site = Site.objects.get_current()
        signup_url = reverse_lazy("customer:register")
        return "http://%s%s?rc=%s" % (current_site.domain, signup_url, self.referral_code)
