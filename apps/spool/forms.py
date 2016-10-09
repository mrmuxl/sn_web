#_*_coding:utf-8_*_
from django import forms
from models import Spool

class SpoolForm(forms.ModelForm):
    class Meta:
        model = Spool
        fields = ['uuid','origin_email','accept_email','origin_uuid','accept_uuid','printer_name','printer_uuid','file_name','file_path','file_client_path','page_num']


