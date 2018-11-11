from django import forms
from django.contrib.auth.forms import (
            UserCreationForm, UserChangeForm)
from django.contrib.auth import get_user_model
      

class RegistrationForm(UserCreationForm):
    # website = forms.URLField(required=False)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password',
                                widget=forms.PasswordInput,
                                required=True,
                                )
    password2 = forms.CharField(label='Confirm Password',
                                widget=forms.PasswordInput,
                                required=True,
                                )
    username = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2',
                  )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.firstname = self.cleaned_data['first_name']
        user.lastname = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


