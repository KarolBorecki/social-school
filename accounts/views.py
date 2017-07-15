from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
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
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('accounts:index')
        else:
            return render(request, self.template_name, {'form': form})
