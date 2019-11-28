from django.conf import settings
from django.utils.timezone import now

from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Applicator(CoreApplicator):

    def get_user_offers(self, user):
        offers = []
        if self.is_birthday(user):
            try:
                offer = ConditionalOffer.active.select_related('condition', 'benefit').get(
                    slug=settings.BIRTHDAY_OFFER_SLUG,
                    offer_type=ConditionalOffer.USER
                )
                offers.append(offer)
            except ConditionalOffer.DoesNotExist:
                pass

        return offers

    def is_birthday(self, user):
        today_date = now().strftime('%d%m')
        user_birthday_date = user.birthday.strftime('%d%m')
        return today_date == user_birthday_date
