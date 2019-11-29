from django.conf.urls import url

import oscar.apps.offer.apps as apps
from oscar.core.loading import get_class


class OfferConfig(apps.OfferConfig):
    name = 'apps.offer'

    def ready(self):
        super().ready()

        self.get_discount_view = get_class('offer.views', 'SetAffiliateAndRedirectView')

    def get_urls(self):
        urls = [
            url(r'^get-discount/(?P<username>[\w-]+)/$', self.get_discount_view.as_view(),
                name='get-discount'),
        ]
        return super().get_urls() + self.post_process_urls(urls)
