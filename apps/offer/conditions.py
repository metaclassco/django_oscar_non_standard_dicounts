from django.utils.timezone import now

from oscar.core.loading import get_model

from apps.offer.models import ConditionIncompatible

Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')


class BirthdayCondition(Condition):
    _description = "User has birthday today."

    class Meta:
        proxy = True

    @property
    def name(self):
        return self._description

    @property
    def description(self):
        return self._description

    def is_satisfied(self, offer, basket):
        if not basket.owner:
            return False
        return basket.owner.date_of_birth == now().date()

    def check_compatibility(self, offer):
        if offer.offer_type != ConditionalOffer.USER:
            raise ConditionIncompatible(
                "Birthday condition could be used only with user type offer."
            )
