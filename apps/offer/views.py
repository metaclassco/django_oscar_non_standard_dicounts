from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView


User = get_user_model()


class SetAffiliateAndRedirectView(RedirectView):
    url = reverse_lazy('catalogue:index')

    def get(self, request, *args, **kwargs):
        self.set_affiliate_in_session(request)
        return super().get(request, *args, **kwargs)

    def set_affiliate_in_session(self, request):
        affiliate = self.kwargs['username']
        if User.objects.filter(username=affiliate).exists():
            affiliate_user = User.objects.get(username=affiliate)
            user = request.user
            if affiliate_user != user and not user.is_affiliate_discount_used:
                request.session[settings.AFFILIATE_SESSION_KEY] = affiliate
                message = (
                    'You have discount from {}. '
                    'You will see it in your basket.'.format(affiliate_user.get_full_name())
                )
                messages.add_message(request, messages.SUCCESS, message)
