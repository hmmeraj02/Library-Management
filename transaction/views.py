from django.shortcuts import render
from .models import Transaction
from .forms import DepositForm
from .constants import DEPOSIT
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.template.loader import render_to_string
# Create your views here.

def send_transaction_email(user, amount, subject, template):
    # Gather users to notify about the transaction
    message = render_to_string(template, {
            'user': user,
            'amount': amount,
        })
    send_email = EmailMultiAlternatives(subject, '', to=[user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()

class DepositView(LoginRequiredMixin, CreateView):
    template_name = 'transactions/deposit_form.html'
    model = Transaction
    form_class = DepositForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
        })
        return kwargs
    
    def get_initial(self):
        initial = {'transaction_type' : DEPOSIT}
        return initial
    
    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        form.instance.user = account
        account.balance += amount
        account.save(
            update_fields = ['balance']
        )
        send_transaction_email(self.request.user, amount, "Deposit Message", "transactions/deposit_email.html")
        return super().form_valid(form)
    
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/report.html'
    model = Transaction
    balance = 0
    context_object_name = 'report_list'

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account = self.request.user.account
        )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.accout,
        })
        return context