from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import auth


# Create your views here.


def home(request):
    context = {}
    if request.user.is_authenticated:
        # Do something for authenticated users.
        context['userStatus'] = 'zalogowany'
    else:
        # Do something for anonymous users.
        context['userStatus'] = 'niezalogowany'
    return render(request, 'home.html', context)

def signup_page(request):
    context = {}
    if request.method == 'POST':
        # Request for sign up
        # Check if user is available
        try:
            user = User.objects.get(username=request.POST['username'])
            context['error'] = 'Podana nazwa użytkownika już istnieje! Proszę podać inną nazwę użytkownika.'
            return render(request, 'auth_system/signup.html', context)
        except User.DoesNotExist:
            # Check if the password1 is equal to the password2
            if request.POST['password1'] != request.POST['password2']:
                context['error'] = 'Podane hasła nie są takie same! Proszę wprowadzić identyczne hasła.'
                return render(request, 'signup.html', context)
            else:
                # Create new user
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                # Automatic login after signing up
                auth.login(request, user)
                # Go to home page
                return redirect('home')
    else:
        return render(request, 'signup.html', context)

def login_page(request):
    context = {}
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'] ,password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            context['error'] = 'Podane hasło lub login są błędne! Podaj poprawne dane.'
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def logout_page(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')