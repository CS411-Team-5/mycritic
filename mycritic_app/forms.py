from django import forms
from mycritic_app.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.movies_rated = 0
        
        if commit:
            user.save()
            
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['user_id', 'movie_id', 'rating']

class MovieForm(forms.Form):
    identifier = forms.CharField(max_length=50)
    title = models.CharField(max_length=100)
    poster = models.CharField(max_length=50)
    description = models.TextField()
