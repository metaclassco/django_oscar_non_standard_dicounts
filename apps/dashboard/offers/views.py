from oscar.apps.dashboard.offers.views import OfferConditionView as CoreOfferConditionView


class OfferConditionView(CoreOfferConditionView):
    def get_form_kwargs(self, *args, **kwargs):
        form_kwargs = super().get_form_kwargs(*args, **kwargs)
        form_kwargs["session_offer"] = self._fetch_session_offer()
        return form_kwargs
