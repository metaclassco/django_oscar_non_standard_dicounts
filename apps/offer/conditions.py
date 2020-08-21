from django.utils.timezone import now

from oscar.core.loading import get_model


Condition = get_model('offer', 'Condition')


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
