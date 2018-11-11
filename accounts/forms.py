from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.forms.models import inlineformset_factory

from .models import UserProfile

User = get_user_model()

class RegistrationForm(UserCreationForm):
    """ Extending the UserCreationForm to specify custom rendering """
    
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
        model = User
        fields = ('first_name',
                  'last_name',
                  'username',
                  'email',
                  'password1',
                  'password2',
                  )

    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields=('picture', 'bio', 'phone', 'website', 'address')
