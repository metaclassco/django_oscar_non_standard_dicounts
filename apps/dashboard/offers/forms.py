from django import forms

from oscar.core.loading import get_model


Benefit = get_model('offer', 'Benefit')


class BenefitForm(forms.ModelForm):

    class Meta:
        model = Benefit
        fields = ['range', 'type', 'value', 'max_affected_items']
