from django import forms
from main.models import CustomUser

class UserForm(forms.ModelForm):
    password_check = forms.CharField(max_length=200, widget=forms.PasswordInput(), label='비밀번호 확인')
    field_order=['username', 'email', 'phone', 'u_id', 'password', 'password_check', 'question_id', 'answer']

    class Meta:
        model = CustomUser
        widgets = {'password':forms.PasswordInput}
        fields = ['username', 'email', 'phone', 'u_id', 'password', 'question_id', 'answer']
        labels = {
            'username': '이름',
            'email': '이메일',
            'phone': '전화번호',
            'u_id': '아이디(사업자번호 10자리)',
            'question_id': '비밀번호 찾기 질문',
            'answer': '답변',
            'password': '비밀번호'
        }