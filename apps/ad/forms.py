#coding=utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _
from models import KxSoftAd,PrinterPop


class AdForm(forms.ModelForm):
    class Meta:
        adform = KxSoftAd


class PrinterPopForm(forms.ModelForm):
    class Meta:
        ppform = PrinterPop
