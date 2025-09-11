from django.conf import settings
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from .forms import CustomeAuthenticationForm
from django.shortcuts import redirect, render
from . import forms

def logout_user(request):
    logout(request)
    return redirect('welcome')

def signup_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # auto-login user
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, 'authentication/signup.html', context={'form': form})

class CustomLoginView(LoginView):
    template_name = "authentication/welcome.html"
    authentication_form = CustomeAuthenticationForm
    redirect_authenticated_user = True 



