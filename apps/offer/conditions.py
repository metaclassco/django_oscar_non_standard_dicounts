from django.conf import settings
from django.utils.timezone import now

from oscar.core.loading import get_model

from apps.offer.models import ConditionIncompatible

Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')


class CustomConditionMixin(object):
    @property
    def name(self):
        return self._description

    @property
    def description(self):
        return self._description


class BirthdayCondition(CustomConditionMixin, Condition):
    _description = "User has birthday today."

    class Meta:
        proxy = True

    def is_satisfied(self, offer, basket, request=None):
        if not basket.owner:
            return False

        current_date = now().date()
        dob = basket.owner.date_of_birth
        return current_date.day == dob.day and current_date.month == dob.month

    def check_compatibility(self, offer):
        if offer.offer_type != ConditionalOffer.USER:
            raise ConditionIncompatible(
                "Birthday condition could be used only with user type offer."
            )


class ReferralCodeCondition(CustomConditionMixin, Condition):
    _description = "User used referral code."

    def is_satisfied(self, offer, basket, request=None):
        referral_code = request.session.get(settings.AFFILIATE_SESSION_KEY, None)
        return referral_code is not None

    def check_compatibility(self, offer):
        if offer.offer_type != ConditionalOffer.SESSION:
            raise ConditionIncompatible(
                "Referral code condition could be used only with session type offer."
            )
