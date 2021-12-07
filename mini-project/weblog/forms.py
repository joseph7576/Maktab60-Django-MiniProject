from django import forms
from .models import *

# login & registration form
class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    # adds 'input100' into every fields class attrs ( for template use only )
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

    # adds 'input100' into every fields class attrs ( for template use only )
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input100'


# post form
class PostForm(forms.ModelForm):
    title = forms.CharField()
    content = forms.CharField(widget=forms.Textarea)
    image = forms.ImageField()
    category = forms.ModelMultipleChoiceField(queryset=Category.objects)
    tag = forms.ModelMultipleChoiceField(queryset=Tag.objects, required=False)

    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tag' , 'status']


# category form
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


# tag form
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'


# comment form
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {
            'text': '',
        }

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = False


# contact form
class ContactForm(forms.Form):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    email_address = forms.EmailField(max_length = 150)
    message = forms.CharField(widget = forms.Textarea, max_length = 2000)