from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.views.generic import CreateView, TemplateView

from accounts.forms import UserRegistrationForm, LoginForm, PasswordResetForm


class IndexView(TemplateView):
    template_name = 'accounts/index.html'


@method_decorator(csrf_protect, name='post')
class LoginView(TemplateView):
    form_class = LoginForm
    template_name = 'accounts/login.html'

    @csrf_protect
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


@method_decorator(csrf_protect, name='post')
@method_decorator(csrf_exempt, name='post')
class RegisterView(CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user_email = form.cleaned_data['email']
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            send_mail(
                'Social School - Email Activation',
                'Link to email activation',
                'karol.boreck@gmail.com',
                [user_email],
                fail_silently=False,
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')
        else:
            return render(request, self.template_name, {'form': form})


@method_decorator(csrf_protect, name='post')
class PasswordResetView(generic.FormView):
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset.html'

    def post(self, request):
        form = self.form_class(request.POST or None)

        if form.is_valid():
            user_email = form.cleaned_data['email']

            if User.objects.filter(email=user_email).exists():
                send_mail(
                    'Social School - Password Reset',
                    form.generate_new_pass(),
                    'Our_email',
                    [user_email],
                    fail_silently=False,
                )
                return redirect('/')
            else:
                raise form.ValidationError("Looks like a user with that email doesn't exists")
        return render(request, self.template_name, {'form': form})


def email_activation_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()

    return render(request, 'accounts/email_activation_successful.html')

