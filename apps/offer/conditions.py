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
                "Birthday condition could be used only with the user type offer."
            )


class ReferralCodeCondition(CustomConditionMixin, Condition):
    """
    Custom condition, which allows referee (referral code applicant) to
    qualify for the discount.
    """

    _description = "User used referral code."

    def is_satisfied(self, offer, basket, request=None):
        if request.user.is_authenticated and request.user.is_referral_code_used:
            return False

        referral_code = request.session.get(settings.REFERRAL_SESSION_KEY, None)
        return referral_code is not None

    def check_compatibility(self, offer):
        if offer.offer_type != ConditionalOffer.SESSION:
            raise ConditionIncompatible(
                "Referral code condition could be used only with the session type offer."
            )


class ReferrerCondition(CustomConditionMixin, Condition):
    """
    Custom condition, which allows referrer (referrer code provider) to
    qualify for the discount. Referrers get discount every time someone
    purchases using their referral codes.
    """

    _description = "Someone purchased using user's referral code."

    def is_satisfied(self, offer, basket, request=None):
        user = basket.owner
        num_offer_applications = offer.get_num_user_applications(user)
        num_referral_code_applications = user.referees.count()
        return num_referral_code_applications > num_offer_applications

    def check_compatibility(self, offer):
        if offer.offer_type != ConditionalOffer.USER:
            raise ConditionIncompatible(
                "Referrer condition could be used only with the user type offer."
            )
