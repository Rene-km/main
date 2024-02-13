from django.views.generic import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import * 
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required

class UserSignupView(CreateView):
    model = User
    form_class = UserSignupForm
    template_name = 'user_signup.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index/')

def index(request):
    return render(request, 'index.html')

class UserLoginView(LoginView):
    template_name='login.html'


def logout_user(request):
    logout(request)
    return redirect("/")





