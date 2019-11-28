from django.views.generic import FormView

from oscar.core.loading import get_model

from .forms import BirthdayBenefitForm


Product = get_model('catalogue', 'Product')
Range = get_model('offer', 'Range')
Condition = get_model('offer', 'Condition')
ConditionalOffer = get_model('offer', 'ConditionalOffer')
Benefit = get_model('offer', 'Benefit')


class BirthdayBenefitUpdateView(FormView):
    form_class = BirthdayBenefitForm
    template_name = 'oscar/dashboard/offers/birthday_benefit_form.html'

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        offer = ConditionalOffer.objects.get(slug='birthday-discount')
        form_kwargs['instance'] = offer.benefit
        return form_kwargs
