#_*_coding:utf-8_*_
from django import forms
from models import Spool

class SpoolForm(forms.ModelForm):
    class Meta:
        spoolform = Spool


