from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import authenticate

from . models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    password_confirm = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name']  #ModelForm automatically adds the modeled fields to the form if it is included in the fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if len(password) < 8:
            raise forms.ValidationError("The password must be at least 8 characters long")


        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

        try:
            validate_password(password)
        except forms.ValidationError as e:
            raise forms.ValidationError(e.messages)
        
        return cleaned_data
    

class LoginForm(forms.Form):
        email = forms.EmailField(required=True)
        password = forms.CharField(widget=forms.PasswordInput, required=True)

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            password = cleaned_data.get("password")

            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            
            cleaned_data['user'] = user
            return cleaned_data