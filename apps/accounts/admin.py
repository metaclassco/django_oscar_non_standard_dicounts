from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as CoreUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(CoreUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'email', 'date_of_birth',
                        'referral_link', 'is_referral_code_used', 'referrer')}
        ),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    readonly_fields = ('referral_link', 'is_referral_code_used', 'referrer')


admin.site.register(User, UserAdmin)
