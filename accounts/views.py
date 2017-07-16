from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView, CreateView


from accounts.forms import UserRegistrationForm


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
            user_email = form.cleaned_data['email']
            user.set_password(password)
            user.is_active = False
            user.save()

            user = authenticate(username=username, password=password)

            send_mail(
                'Social School - Email confirmation ',
                'MSG',
                'our.email@shit.eu',
                [user_email],
                fail_silently=False,
            )

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:index')
        else:
            return render(request, self.template_name, {'form': form})


def email_activation_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.is_active = True
    user.save()

    return render(request, 'accounts/email_activation_successful.html')
