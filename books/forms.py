from django import forms
from django.core.exceptions import ValidationError
from .models import *

class AddBookForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Category not selected'

    class Meta:
        model = Books
        # fields = '__all__'
        fields = ['title', 'slug', 'author', 'description', 'photo', 'is_published', 'cat']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'slug': forms.TextInput(attrs={'class': 'form-input'}),
            'author': forms.Textarea(attrs={'cols': 39, 'rows': 5, 'style':'resize:none'}),
            'description': forms.Textarea(attrs={'cols': 39, 'rows': 10, 'style':'resize:none'}),
        }
    
    def clean_title(self):
        ''' User validator '''
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('The title is longer than 200 characters')
        
        return title