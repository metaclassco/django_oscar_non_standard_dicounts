from oscar.apps.offer.abstract_models import AbstractCondition, AbstractConditionalOffer


class ConditionIncompatible(Exception):
    pass


class ConditionalOffer(AbstractConditionalOffer):
    def apply_benefit(self, basket, request=None):
        if not self.is_condition_satisfied(basket, request=request):
            return ZERO_DISCOUNT
        return self.benefit.proxy().apply(basket, self.condition.proxy(), self)

    def is_condition_satisfied(self, basket, request=None):
        return self.condition.proxy().is_satisfied(self, basket, request=request)


class Condition(AbstractCondition):
    def is_satisfied(self, offer, basket, request=None):
        return super().is_satisfied(offer=offer, basket=basket)

    def check_compatibility(self, offer):
        proxy_instance = self.proxy()
        check_compatibility = getattr(proxy_instance, "check_compatibility", None)
        if check_compatibility is not None and callable(check_compatibility):
            proxy_instance.check_compatibility(offer)


from oscar.apps.offer.models import *  # noqa isort:skip
