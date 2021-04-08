from django.contrib.auth.models import User
from .models import *
from django import forms


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'restrict_comment',)


class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('body', 'restrict_comment',)


class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput(
        attrs={'placeholder': 'Enter username...'}))
    password = forms.CharField(label="", widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password...'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm Password...'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Password Missmatch')
        return confirm_password


class UserEditForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))
    email = forms.CharField(widget=forms.TextInput(
        attrs={'readonly': 'readonly'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)


class CommentForm(forms.ModelForm):
    content = forms.CharField(label="", widget=forms.Textarea(
        attrs={'class': 'form-control',
               'style': 'background-color: black; color: white; border: none; border-radius: 999px; outline-width: 0;',
               'placeholder': 'Write a comment', 'rows': '1', 'cols': '20', }))

    class Meta:
        model = Comment
        fields = ('content',)
