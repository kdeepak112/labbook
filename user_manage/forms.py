from django import forms
from django.forms import ModelForm
from .models import fileUpload
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class fileUploaded(ModelForm):
    class Meta:
        # file = forms.FileField(widget=forms.TextInput(
        #     attrs={'name': 'file_upload'}))
        model = fileUpload
        fields = ['file']



class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')
