from typing import ClassVar
from django import forms
from django.contrib.auth.models import User
from django.db.models import fields
from .models import Profile


class UserLoginForm(forms.Form):
    # forms.Form类适用于不与数据库直接交互的功能
    username = forms.CharField()
    password = forms.CharField()


class UserRegisterForm(forms.ModelForm):
    # forms.ModelForm类适用于与数据库直接交互的功能
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        # 有点没懂Meta到底是干什么用的
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        # def clean_[字段]
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError('密码输入不一致，请重试。')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio')
