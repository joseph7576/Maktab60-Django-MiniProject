from django import forms
from django.contrib.auth.models import User
from django.forms import fields, widgets
from django.http import request
from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'

class RegisterForm(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['first_name', 'last_name', 'username', 'email']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'

class PostForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    category = forms.ModelMultipleChoiceField(queryset=Category.objects)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects, required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tag' , 'status']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
