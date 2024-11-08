from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import LoginForm
from django.http import HttpResponseRedirect
from django.views.generic import View


class LoginView(View):
    template_name = 'users/login.html'
    form_class = LoginForm

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )
            print('valid')

            if user is not None:
                login(request, user)
                return redirect(reverse_lazy('student-create'))

        message = 'Invalid Username or Password!'
        return render(request, self.template_name, context={'message': message})



class __LoginTamplateView(TemplateView):
    template_name = 'users/login.html'


class __UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('student-create')

    def form_valid(self, form):

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Invalid username and password')
            plain_error_message = "erro hapend"
            return super().form_invalid(form)
