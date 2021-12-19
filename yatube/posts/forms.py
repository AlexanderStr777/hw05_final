# posts/forms.py
from django import forms
from django.core.exceptions import ValidationError

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')

    def clean_text(self):
        text = self.cleaned_data['text']
        if text:
            return text
        raise ValidationError('Это поле обязательно')

    def clean_group(self):
        group = self.cleaned_data['group']
        return group


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)

    def clean_text(self):
        text = self.cleaned_data['text']
        if text:
            return text
        raise ValidationError('Это поле обязательно')
