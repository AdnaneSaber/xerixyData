from django import forms
from django.contrib.auth.models import User
from django.db.models.base import Model
from django.forms.models import ModelForm

from .models import Articles, UserProfile


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('age', 'city', 'avatar')


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def save(self, commit=True):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password'])
        # new_user.first_name = self.cleaned_data['first_name']
        # new_user.last_name = self.cleaned_data['last_name']
        if commit:
            new_user.save()
        return new_user


class ArticleForm(ModelForm):
    class Meta:
        model = Articles
        fields = ('price', 'name', 'category', 'avatar')
