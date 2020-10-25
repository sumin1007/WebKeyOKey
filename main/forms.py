from django import forms
from .models import CustomUser
#from django.contrib.auth.models import User

class SigninForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        widgets = {'password':forms.PasswordInput}
        fields = ['u_id', 'password']

        labels = {
            'u_id': '아이디(사업자번호 10자리)',
            'password': '비밀번호'
        } 