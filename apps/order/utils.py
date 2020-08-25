from django.conf import settings
from django.contrib.auth import get_user_model

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
        super().record_discount(discount)

        if settings.AFFILIATE_SESSION_KEY in self.request.session.keys():
            self.user.is_referral_code_used = True
            self.user.save()

            del self.request.session[settings.AFFILIATE_SESSION_KEY]
