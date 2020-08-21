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

    def get_session_offers(self, request):
        offers = []
        affiliate = request.session.get(settings.AFFILIATE_SESSION_KEY, None)
        if affiliate is not None:
            offer = ConditionalOffer.active.select_related('condition', 'benefit').get(
                slug=settings.AFFILIATE_OFFER_SLUG,
                offer_type=ConditionalOffer.SESSION
            )
            offers.append(offer)
        return offers

    def is_birthday(self, user):
        if user.is_anonymous:
            return False

        today_date = now().strftime('%d%m')
        user_birthday_date = user.date_of_birth.strftime('%d%m')
        return today_date == user_birthday_date
