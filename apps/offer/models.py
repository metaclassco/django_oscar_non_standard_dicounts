from oscar.apps.offer.abstract_models import AbstractCondition


class ConditionIncompatible(Exception):
    pass


class Condition(AbstractCondition):
    def check_compatibility(self, offer):
        proxy_instance = self.proxy()
        check_compatibility = getattr(proxy_instance, "check_compatibility", None)
        if check_compatibility is not None and callable(check_compatibility):
            proxy_instance.check_compatibility(offer)


from oscar.apps.offer.models import *  # noqa isort:skip
