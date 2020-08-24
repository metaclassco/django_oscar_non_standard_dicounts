from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView


User = get_user_model()


class SetReferralCodeAndRedirectView(RedirectView):
    url = reverse_lazy('catalogue:index')

    def get(self, request, *args, **kwargs):
        referral_code = self.kwargs.get('referral_code', None)
        if referral_code:
            if User.objects.filter(referral_code=referral_code).exists():
                request.session[settings.AFFILIATE_SESSION_KEY] = referral_code
                messages.success(request, "Your referral code is valid, discount will be applied on checkout.")
            else:
                messages.error(request, "Referrer account not found.")
        else:
            messages.error(request, "Referral code is not provided.")
        return super().get(request, *args, **kwargs)
