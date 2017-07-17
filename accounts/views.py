from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import CreateView, TemplateView

from accounts.forms import UserRegistrationForm, LoginForm


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


@method_decorator(csrf_protect, name='post')
class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


def email_activation_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()

    return render(request, 'accounts/email_activation_successful.html')


class LoginView(TemplateView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})

    def get(self, request):
        form = self.form_class(request.POST or None)
        return render(request, self.template_name, {'form': form})

