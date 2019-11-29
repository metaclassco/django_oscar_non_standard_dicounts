from django.conf import settings
from django.views.generic import FormView

from oscar.core.loading import get_model

from .forms import BenefitForm


Product = get_model('catalogue', 'Product')
Range = get_model('offer', 'Range')
Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')
Benefit = get_model('offer', 'Benefit')


class BenefitUpdateMixin(FormView):
    form_class = BenefitForm
    template_name = 'oscar/dashboard/offers/benefit_form.html'
    slug = None

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        offer = ConditionalOffer.objects.get(slug=settings.BIRTHDAY_OFFER_SLUG)
        form_kwargs['instance'] = offer.benefit
        return form_kwargs


class BirthdayBenefitUpdateView(BenefitUpdateMixin):
    slug = settings.BIRTHDAY_OFFER_SLUG
