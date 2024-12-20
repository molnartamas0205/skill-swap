from django import forms
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import authenticate

from .models import Category, CustomUser, TargetAudience, TutoringService

class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username',
                               widget=forms.TextInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Username'}),
                               required=True)
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control',
                                                           'placeholder': 'Email'}),
                             required=True)
    full_name = forms.CharField(label='Full Name',
                                widget=forms.TextInput(attrs={'class': 'form-control',
                                                            'placeholder': 'Full Name'}),
                                required=True)
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                'placeholder': 'Password'}),
                               required=True)
    password_confirm = forms.CharField(label='Confirm Password',
                                       widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                        'placeholder': 'Confirm Password'}),
                                       required=True)

    class Meta:
        model = CustomUser
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
        email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control',
                                                                               'placeholder': 'Email'
                                                                               }),
                                 required=True)
        password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                                       'placeholder': 'Password'
                                                                                       }),
                                   required=True)

        def clean(self):
            cleaned_data = super().clean()
            email = cleaned_data.get("email")
            password = cleaned_data.get("password")

            user = authenticate(email=email, password=password)

            if user is None:
                raise forms.ValidationError("Invalid email or password.")
            
            cleaned_data['user'] = user
            return cleaned_data
        
class AdvertisementForm(forms.ModelForm):
    target_audiences = forms.ModelMultipleChoiceField(
        queryset=TargetAudience.objects.all(),
        required = True,
    )

    class Meta:
        model = TutoringService
        fields = ['title', 'description', 'category', 'price', 'available', 'target_audiences']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control',
                                         'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'rows': 5,
                                                 'class': 'form-control',
                                                 'placeholder': 'Description'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'step': 5,
                                              'class': 'form-control',
                                              'placeholder': 'Price'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'target_audiences': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'title': 'Advertisement Title',
            'description': 'Description',
            'category': 'Category',
            'price': 'Price (USD)',
            'target_audiences': 'Target Audience',
        }
