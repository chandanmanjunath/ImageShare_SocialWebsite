#Import forms from django
from django import forms

#Import user from auth framework model
from django.contrib.auth.models import User
from .models import Profile

class LoginForm(forms.Form):
    username = forms.CharField()
    #To use passord input specify widget=forms.PasswordInput
    password = forms.CharField(widget=forms.PasswordInput)

#Defining the new registration form
class UserRegistrationForm(forms.ModelForm):

        password = forms.CharField(label='Password',
                                   widget=forms.PasswordInput)
        password2 = forms.CharField(label='Repeat password',
                                    widget=forms.PasswordInput)
        #Class meta is used to specify any fields other than form fields
        class Meta:
                #use imported user model
                model = User
                #Include the below set of fields in form
                fields = ('username', 'first_name', 'email')
        #The below method is written to verify the two entered passwords
        def clean_password2(self):
            #get the form field data from cleaned_data dictionay to cd variable
            cd = self.cleaned_data
            #if first and second password are not sa,e raise validation error
            if cd['password'] != cd['password2']:
                raise forms.ValidationError('Passwords don\'t match.')
            #return the second password
            return cd['password2']



class UserEditForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ('date_of_birth', 'photo')



            
