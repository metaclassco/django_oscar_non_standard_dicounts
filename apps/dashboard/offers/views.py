from django.conf import settings
from django.urls import reverse_lazy
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
        offer = ConditionalOffer.objects.get(slug=self.slug)
        form_kwargs['instance'] = offer.benefit
        return form_kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BirthdayBenefitUpdateView(BenefitUpdateMixin):
    success_url = reverse_lazy('dashboard:birthday-benefit-update')
    slug = settings.BIRTHDAY_OFFER_SLUG


class AffiliateBenefitUpdateView(BenefitUpdateMixin):
    success_url = reverse_lazy('dashboard:affiliate-benefit-update')
    slug = settings.AFFILIATE_OFFER_SLUG
