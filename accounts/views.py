from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, CreateView, TemplateView

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
