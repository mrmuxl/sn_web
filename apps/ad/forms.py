#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import KxSoftAd


class AdForm(forms.ModelForm):
    class Meta:
        adform = KxSoftAd

