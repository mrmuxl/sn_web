#_*_coding:utf-8_*_

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils import timezone

from kx.models import KxUser


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label=u'请输入密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'请再输入一次', widget=forms.PasswordInput)

    class Meta:
        model = KxUser
        fields = ('email', 'nick')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        now = timezone.now()
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.create_time = now
        user.update_time = now
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = KxUser

    def clean_password(self):
        return self.initial["password"]

#class AdminPasswordChangeForm(forms.ModelForm):
#    """
#    在Admin接口更改用户密码
#    """
#    error_messages = { u'密码不匹配':_(u"两次输入的密码不匹配")
#    password1 = forms.CharField(label=_(u"请输入密码"),widget=forms.PasswordInput)
#    password2 = forms.CharField(label=_(u"请再次输入密码"),widget=forms.PasswordInput)
#
#    class Meta:
#        model = KxUser
#
#    def clean_password(self):
#        password1 = self.cleaned_data.get('password1')
#        password2 = self.cleaned_data.get('password2')
#        if password1 and password2:
#            if password1 != password2:
#                raise forms.ValidationError(self,error_message[u'密码不匹配'])
#        return password2
#
#    def save(self,commit=True):
#    """
#        保存新的密码
#    """
#        now = timezone.now()
#        # Save the provided password in hashed format
#        user = super(UserCreationForm, self).save(commit=False)
#        user.set_password(self.cleaned_data["password1"])
#        user.create_time = now
#        user.update_time = now
#        if commit:
#            user.save()
#        return user
