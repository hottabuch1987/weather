from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm



class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('weather')

    def form_invalid(self, form):
        print(form.errors) 

    
   

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'account/login.html'

    def get_success_url(self):
        return reverse_lazy('weather')


def logout_user(request):
    logout(request)
    return redirect('login')


