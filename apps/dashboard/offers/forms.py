from django import forms
from django.utils.translation import gettext_lazy as _

from oscar.apps.dashboard.offers.forms import ConditionForm as CoreConditionForm
from oscar.core.loading import get_model

from apps.offer.models import ConditionIncompatible


Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')

# Voucher offer type deliberately excluded, since voucher offer types created through
# the dedicated dashboard view.
OFFER_TYPE_CHOICES = (
    (ConditionalOffer.SITE, _("Site offer - available to all users")),
    (ConditionalOffer.USER, _("User offer - available to certain types of user")),
    (ConditionalOffer.SESSION, _("Session offer - temporary offer, available for "
                                 "a user for the duration of their session")),
)


class MetaDataForm(forms.ModelForm):
    offer_type = forms.ChoiceField(choices=OFFER_TYPE_CHOICES)

    class Meta:
        model = ConditionalOffer
        fields = ('name', 'description', 'offer_type')


class ConditionForm(CoreConditionForm):
    def __init__(self, *args, **kwargs):
        self.session_offer = kwargs.pop("session_offer", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        data = super().clean()
        custom_condition = data.get("custom_condition", None)
        if custom_condition:
            condition = Condition.objects.get(id=custom_condition)
            try:
                condition.check_compatibility(offer=self.session_offer)
            except ConditionIncompatible as e:
                raise forms.ValidationError(e)
        return data
