from oscar.apps.offer.applicator import Applicator as CoreApplicator
from oscar.core.loading import get_class, get_model


ConditionalOffer = get_model('offer', 'ConditionalOffer')
OfferApplications = get_class('offer.results', 'OfferApplications')


class Applicator(CoreApplicator):
    def apply(self, basket, user=None, request=None):
        offers = self.get_offers(basket, user, request)
        self.apply_offers(basket, offers, request)

    def _get_offers_by_type(self, offer_type):
        qs = ConditionalOffer.active.filter(offer_type=offer_type)
        return qs.select_related('condition', 'benefit')

    def get_user_offers(self, user):
        return self._get_offers_by_type(offer_type=ConditionalOffer.USER)

    def get_session_offers(self, request):
        return self._get_offers_by_type(offer_type=ConditionalOffer.SESSION)

    def apply_offers(self, basket, offers, request):
        applications = OfferApplications()
        for offer in offers:
            num_applications = 0
            while num_applications < offer.get_max_applications(basket.owner):
                result = offer.apply_benefit(basket, request=request)
                num_applications += 1
                if not result.is_successful:
                    break
                applications.add(offer, result)
                if result.is_final:
                    break

        basket.offer_applications = applications
