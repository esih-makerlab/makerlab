from django import forms
from django.utils.translation import gettext_lazy as _

class AttendeeForm(forms.Form):
    first_name = forms.CharField(
        label=_('Prénom'), required=True
    )
    last_name = forms.CharField(
        label=_('Nom'), required=True
    )
    telephone = forms.CharField(
        label=_('Telephone'),max_length=8, required=True, help_text=_('Ex: +509XXXXXXXX')
    )
    email = forms.EmailField(
        label=_('Email'), widget=forms.EmailInput,help_text=_('Votre email Ex:john@winterfell.got'),required=True
    )
    address = forms.CharField(
        label=_('Addresse'),required=True,help_text=_('Ex:29, 2e ruelle Nazon, Route de Bourdon, Port-au-Prince')
    )



    
