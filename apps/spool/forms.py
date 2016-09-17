#_*_coding:utf-8_*_
from django import forms
from models import Spool

class SpoolForm(forms.ModelForm):
    class Meta:
        model = Spool
        fields = ['uuid','origin_email','accept_email','origin_uuid','accept_uuid']


