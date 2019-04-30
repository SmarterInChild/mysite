from django import forms
from django.contrib.auth.models import User
from .models import UserProfile, UserInfo

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')

class RegistrationForm(forms.ModelForm):
    # username = forms.CharField(label='用户名')
    # email = forms.CharField(label='邮箱')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    password2 = forms.CharField(widget=forms.PasswordInput, label='重复密码')

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password2(self):
        forms_data = self.cleaned_data
        if forms_data['password'] != forms_data['password2']:
            raise forms.ValidationError(('重复输入的密码不匹配'), code='matchError')
        return forms_data['password2']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['birth', 'phone']
        
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['school', 'company', 'profession', 'address', 'aboutme']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

