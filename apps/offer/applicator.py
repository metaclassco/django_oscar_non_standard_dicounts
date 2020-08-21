from django.conf import settings

from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Applicator(CoreApplicator):

    def get_user_offers(self, user):
        qs = ConditionalOffer.active.filter(offer_type=ConditionalOffer.USER)
        return qs.select_related('condition', 'benefit')

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
