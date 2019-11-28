from django.conf.urls import url

import oscar.apps.dashboard.offers.apps as apps
from oscar.core.loading import get_class


class OffersDashboardConfig(apps.OffersDashboardConfig):
    label = 'offers_dashboard'
    name = 'apps.dashboard.offers'
    verbose_name = 'Offers dashboard'

    def ready(self):
        super().ready()
        self.birthday_benefit_update_view = get_class('dashboard.offers.views', 'BirthdayBenefitUpdateView')

    def get_urls(self):
        urls = [
            url(r'^birthday-benefit/update/$', self.birthday_benefit_update_view.as_view(),
                name='birthday-benefit-update'),
        ]
        return super().get_urls() + self.post_process_urls(urls)
