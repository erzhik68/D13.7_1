from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Ad, Category


# Создаём модельную форму
# class AdForm(ModelForm):
#     class Meta:
#         model = Ad
#         fields = '__all__'
        # fields = ['category', 'title', 'poster', 'text', 'video']
        # widgets = {
        #     'category': CheckboxSelectMultiple(),
        # }

class AdForm(forms.Form):
    author = forms.ModelChoiceField(queryset=User.objects.all())
    category = forms.ModelChoiceField(queryset=Category.objects.all())
    title = forms.CharField(max_length=100)
    poster = forms.ImageField()
    text = forms.CharField()
    video = forms.Media

class CommentForm(ModelForm):
    pass
#     class Meta:
#         model = Comment
#         fields = ['comment_author', 'email', 'comment_text']
