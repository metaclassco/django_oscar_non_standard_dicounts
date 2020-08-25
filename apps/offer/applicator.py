from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')


class Applicator(CoreApplicator):

    def get_user_offers(self, user):
        qs = ConditionalOffer.active.filter(offer_type=ConditionalOffer.USER)
        return qs.select_related('condition', 'benefit')

    def get_session_offers(self, request):
        offers = []
        qs = ConditionalOffer.active.filter(offer_type=ConditionalOffer.USER)
        qs = qs.select_related('condition', 'benefit')
        for offer in qs:
            if offer.is_condition_satisfied(basket=request.basket, request=request):
                offers.append(offer)
        return offers
