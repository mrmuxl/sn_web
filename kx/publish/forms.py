#_*_coding:utf-8_*_
from django import forms
from kx.models import KxPub

class PublishAdd(forms.Form):
    ver = forms.CharField(max_length=20,error_messages={'required':u'请填写版本号'})
    desc = forms.CharField(widget=forms.Textarea(attrs={'class':'desc_area','style':'width:300px;height:100px'}))
    ins = forms.FileField(label=u"安装包:",required=False)
    patch = forms.FileField(label=u"补丁包:",required=False)
    id = forms.IntegerField(widget=forms.HiddenInput,required=False)
    def clean_ver(self):
        ver = self.cleaned_data.get('ver')
        ver_obj = KxPub.objects.all().values('ver')
        ver_list = [ i['ver'] for i in ver_obj]
        if not ver:
            raise forms.ValidationError(u'请填写版本号！')
        #if ver in ver_list:
        #    raise forms.ValidationError(u'版本号已经存在,不能设置一个已经存在的版本号')
        return ver
    def clean_desc(self):
        desc = self.cleaned_data.get('desc')
        if not desc:
            raise forms.ValidationError(u'请填写功能描述！')
        return desc
