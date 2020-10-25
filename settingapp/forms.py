from django import forms
from main.models import Menu, Option, CustomUser

class AddForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['m_name', 'c_id', 'm_info', 'm_img', 'm_price', 'm_takeout', 'options']

class EditForm(forms.ModelForm):
    class Meta:
        model = Menu
        fields = ['m_name', 'c_id', 'm_info', 'm_img', 'm_price', 'm_takeout','options']

class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = ['option_name', 'option_price']

class CustomForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['u_id']