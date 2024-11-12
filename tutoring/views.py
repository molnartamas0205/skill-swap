from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate

from .models import CustomUser, CustomUserManager
from . forms import LoginForm, RegistrationForm



# Create your views here.


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home') 
            else:
                form.add_error(None, "Invalid email or password")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            username = form.cleaned_data["username"]
            full_name = form.cleaned_data["full_name"]
            
            user = CustomUser.objects.create_user(username = username, email=email, password=password, full_name=full_name)
            login(request, user)
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to the home page after logout

def tutor_list_view(request, *args, **kwargs):
    return render(request, 'tutor_list.html', {})

