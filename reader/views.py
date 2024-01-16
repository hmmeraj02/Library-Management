from typing import Any
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.views.generic import CreateView, FormView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from book.models import Book

# Create your views here.

class UserRegistrationView(FormView):
    template_name = 'accounts/register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        # print(form.cleaned_data)
        user = form.save()
        # login(self.request, user)
        # print(user)
        return super().form_valid(form)
    
class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    def get_success_url(self):
        return reverse_lazy('homepage')
    
@login_required
def profile(request):
    books = Book.objects.filter(borrower=request.user)
    return render(request, 'accounts/profile.html', {'books':books})

def user_logout(request):
    logout(request)
    return redirect('login')