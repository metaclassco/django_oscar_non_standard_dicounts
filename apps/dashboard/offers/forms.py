from django import forms

from oscar.core.loading import get_model
from django.utils.translation import gettext_lazy as _


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
