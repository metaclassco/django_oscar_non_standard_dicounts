from django.conf.urls import url

import oscar.apps.offer.apps as apps


class OfferConfig(apps.OfferConfig):
    name = 'apps.offer'

    def get_urls(self):
        from .views import SetReferralCodeAndRedirectView

        urls = [
            url(r'^rp/(?P<referral_code>[\w-]+)$', SetReferralCodeAndRedirectView.as_view(),
                name='apply_referral_code'),
        ]
        return super().get_urls() + self.post_process_urls(urls)
