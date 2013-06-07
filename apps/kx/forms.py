#coding=utf-8
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from kx.models import KxUser

class RegisterForm(forms.Form):
    email=forms.EmailField(label=_(u"邮件"),max_length=30,widget=forms.TextInput(attrs={'size': 30,}))    
    username=forms.CharField(label=_(u"昵称"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"密码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    password1=forms.CharField(label=_(u"密码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    
    def clean_username(self):
        '''验证重复昵称'''
        users = KxUser.objects.filter(username__iexact=self.cleaned_data["username"])
        if not users:
            return self.cleaned_data["username"]
        raise forms.ValidationError(_(u"该昵称已经被使用请使用其他的昵称"))
        
    def clean_email(self):
        '''验证重复email'''
        emails = KxUser.objects.filter(email__iexact=self.cleaned_data["email"])
        if not emails:
            return self.cleaned_data["email"]
        raise forms.ValidationError(_(u"该邮箱已经被使用请使用其他的"))
    def clean_password(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password and password1 and password != password2:
            raise forms.ValidationError(u"两次输入密码不匹配")
        
class LoginForm(forms.Form):
    username=forms.CharField(label=_(u"昵称"),max_length=30,widget=forms.TextInput(attrs={'size': 20,}))
    password=forms.CharField(label=_(u"密码"),max_length=30,widget=forms.PasswordInput(attrs={'size': 20,}))
    
