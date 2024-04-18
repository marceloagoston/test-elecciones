from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm


def custom_logout(request):
    logout(request)
    return redirect('login')
