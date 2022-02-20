from email import message
from tkinter.ttk import Label
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from accounts.models import UserProfile,User
from django import  forms


class UserProfileForm(UserCreationForm):

    class Meta:
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2',)
        model = User
    #     widgets = {
    #     'password': forms.PasswordInput(),
    #     'confirm_password': forms.PasswordInput(),
    # }

        # def __init__(self, *args, **kwargs):
        #     super().__init__(*args, **kwargs)
        #     self.fields['username'].label = 'Display Name'
        #     self.fields['email'].label = 'Email Address'
        # def clean(self):
        #     cleaned_data = super(UserProfileForm, self).clean()
        #     password = cleaned_data.get("password")
        #     confirm_password = cleaned_data.get("confirm_password")

        #     if password != confirm_password:
        #         raise forms.ValidationError(
        #         "password and confirm_password does not match"
        #     )


class ProfileCreateForm(forms.ModelForm):
    class Meta:
        model= UserProfile
        fields =('first_name', 'last_name','phone_number', 'gender', 'city', 'state', 'country', 'Hobbies', 'Languages','image')


class Threadform(forms.Form):
    username = forms.CharField(label='', max_length=100)

class Messageform(forms.Form):
    message = forms.CharField(label='', max_length=1000)

class LocationForm(forms.Form):
    radius = forms.IntegerField(label='')