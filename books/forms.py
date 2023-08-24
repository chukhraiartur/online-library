from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.utils.text import slugify
from captcha.fields import CaptchaField
from dal import autocomplete

from .models import *

class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Category not selected'

    class Meta:
        model = Books
        fields = ('title', 'author', 'description', 'photo', 'pdf_file', 'is_published', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 39, 'rows': 10, 'style': 'resize:none', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        ''' User validator '''
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('The title is longer than 200 characters')

        return title
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)  # Slug generation based on the name
        if commit:
            instance.save()
        return instance

class EditBookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ('title', 'author', 'description', 'photo', 'pdf_file', 'is_published', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'cols': 39, 'rows': 10, 'style': 'resize:none', 'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'pdf_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'is_published': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cat': forms.Select(attrs={'class': 'form-select'}),
        }

    def clean_title(self):
        ''' User validator '''
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise forms.ValidationError('The title is longer than 200 characters')
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)  # Генерация слага на основе названия
        if commit:
            instance.save()
        return instance

class SignUpUserForm(UserCreationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignInUserForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class ContactForm(forms.Form):
    name = forms.CharField(label='Name', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=255)
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'style':'resize:none', 'class': 'form-control'}))
    captcha = CaptchaField()

class BookSearchForm(forms.Form):
    search_query = forms.CharField(
        label='Search',
        widget=autocomplete.ListSelect2(url='autocomplete')
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

class BooksForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['title', 'author', 'description', 'photo', 'pdf_file', 'cat']
