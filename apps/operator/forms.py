#_*_coding:utf-8_*_

from django import forms
from models import Operator

class OperatorForm(forms.Form):
    class Meta:
        operator = Operator

