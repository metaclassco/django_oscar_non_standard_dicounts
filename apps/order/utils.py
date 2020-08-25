import logging

from django.conf import settings
from django.contrib.auth import get_user_model

from oscar.apps.order.utils import OrderCreator as OriginalOrderCreator
from oscar.core.loading import get_model


logger = logging.getLogger(__file__)
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
        super().record_discount(discount)

        referral_code = self.request.session.get(settings.REFERRAL_SESSION_KEY, None)

        if referral_code:
            try:
                referrer = User.objects.get(referral_code=referral_code)
            except User.DoesNotExist:
                referrer = None
                logger.error("Could not retrieve referrer for referral code '%s'", referrer)

            self.user.is_referral_code_used = True
            self.user.referrer = referrer
            self.user.save()

            del self.request.session[settings.REFERRAL_SESSION_KEY]
