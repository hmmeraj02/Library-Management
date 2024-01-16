from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ReaderAccount

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name','last_name', 'email']

    def save(self, commit=True):
        our_user = super().save(commit=False)
        if commit is True:
            our_user.save()
            ReaderAccount.objects.create(
                user=our_user,
                account_no = 1000 + our_user.id
                # balance = self.cleaned_data['balance']
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
