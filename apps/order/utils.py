from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import F

from oscar.apps.order.utils import OrderCreator as OriginalOrderCreator
from oscar.core.loading import get_model


User = get_user_model()
Order = get_model('order', 'Order')


class OrderCreator(OriginalOrderCreator):
    user = None
    request = None

    def place_order(self, *args, **kwargs):
        self.user = kwargs.get('user', None)
        self.request = kwargs.get('request', None)
        return super().place_order(*args, **kwargs)

    def record_discount(self, discount):
        if discount['offer'].slug == settings.AFFILIATE_OFFER_SLUG:
            self.record_affiliate_discount_usage()

    def record_affiliate_discount_usage(self):
        self.user.is_affiliate_discount_used = True
        self.user.save()

        if settings.AFFILIATE_SESSION_KEY in self.request.session.keys():
            affiliate_username = self.request.session[settings.AFFILIATE_SESSION_KEY]
            affiliate = User.objects.get(username=affiliate_username)
            affiliate.bonuses = F('bonuses') + settings.AFFILIATE_BONUSES
            affiliate.save()

            del self.request.session[settings.AFFILIATE_SESSION_KEY]
