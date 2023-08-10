from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField

from .models import *


class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Category not selected'

    class Meta:
        model = Books
        fields = ['title', 'slug', 'author', 'description', 'photo', 'is_published', 'cat']     # fields = '__all__'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'author': forms.Textarea(attrs={'cols': 39, 'rows': 5, 'style':'resize:none', 'class': 'form-input'}),
            'description': forms.Textarea(attrs={'cols': 39, 'rows': 10, 'style':'resize:none', 'class': 'form-input'}),
        }
    
    def clean_title(self):
        ''' User validator '''
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('The title is longer than 200 characters')
        
        return title
    

class SignUpUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SignInUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-input'}), max_length=255)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'style':'resize:none', 'class': 'form-input'}))
    captcha = CaptchaField()