from django import forms
from .models import Transaction
from .constants import DEPOSIT

class DepositForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit = True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()
    
    def clean_amount(self):
        min_deposit_amount = 500
        amount = self.cleaned_data.get('amount')
        if amount < min_deposit_amount:
            raise forms.ValidationError(f"Deposits must be at least ${min_deposit_amount}")
        return amount
