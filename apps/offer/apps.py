from django.conf.urls import url

import oscar.apps.offer.apps as apps

from .views import SetReferralCodeAndRedirectView


class OfferConfig(apps.OfferConfig):
    name = 'apps.offer'

    def get_urls(self):
        urls = [
            url(r'^rp/(?P<referral_code>[\w-]+)$', SetReferralCodeAndRedirectView.as_view(), name='referral_program'),
        ]
        return super().get_urls() + self.post_process_urls(urls)
