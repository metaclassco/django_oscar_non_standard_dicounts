from oscar.core.loading import get_class

CoreOfferConditionView = get_class("dashboard.offers.views", "OfferConditionView")


class OfferConditionView(CoreOfferConditionView):
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["session_offer"] = self._fetch_session_offer()
        return form_kwargs
