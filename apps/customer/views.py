from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model

from oscar.apps.customer.views import AccountRegistrationView as CoreAccountRegistrationView


User = get_user_model()


class AccountRegistrationView(CoreAccountRegistrationView):
    referral_code = None

    def dispatch(self, request, *args, **kwargs):
        referral_code = request.GET.get('rc', None)
        if referral_code:
            if User.objects.filter(referral_code=referral_code).exists():
                self.referral_code = referral_code
            else:
                messages.error(request, "Referrer account not found.")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        r = super().form_valid(form)
        if self.referral_code:
            self.request.session[settings.REFERRAL_SESSION_KEY] = self.referral_code
            messages.success(self.request, "Your referral code is valid, discount will be applied on checkout.")
        return r
