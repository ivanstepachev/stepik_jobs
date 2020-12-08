from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from jobs.forms import LoginForm, NewUser


class RegisterView(CreateView):
    form_class = NewUser
    success_url = '/login/'
    template_name = 'jobs/authorization/register.html'


class LoginView(LoginView):
    form_class = LoginForm
    redirect_authenticated_user = True
    template_name = 'jobs/authorization/login.html'
