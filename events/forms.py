# events/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Event, Media, Category

class RegistrationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student','Student'),
        ('faculty','Faculty'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES)
    class Meta:
        model = User
        fields = ['username','email','password1','password2','role']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','date']

class MediaForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = ['file','media_type','event','description','category']
        widgets = {
            'media_type': forms.Select(),
            'event': forms.Select(),
            'category': forms.Select()
        }
