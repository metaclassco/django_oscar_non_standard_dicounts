from django.conf.urls import url

import oscar.apps.offer.apps as apps


class OfferConfig(apps.OfferConfig):
    name = 'apps.offer'
