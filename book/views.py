from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import DetailView
from . import models
from . import forms
from .models import Book, Review
from .forms import BookForm, ReviewForm
from transaction.models import Transaction
from transaction.constants import BORROW, RETURN
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
# Create your views here.

class BookDetailView(DetailView):
    model = models.Book
    pk_url_kwarg = 'pk'
    template_name = "book_detail.html"

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        review_form = forms.ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.book = book
            new_review.save()
        return self.get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        reviews = book.reviews.all()
        review_form = forms.ReviewForm()
        context["reviews"] = reviews
        context['review_form'] = review_form
        return context

@login_required
def add_review(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user 
            review.save()
            return redirect('book_detail', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'book_review.html', {'form': form, 'book': book})

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    account = request.user.account
    if account.balance < book.price:
        messages.error(request, "You don't have enough money to borrow this book.")
        return redirect('profile')
    book.save()
    book.borrower.add(request.user)
    Transaction.objects.create(
        user = request.user.account,
        amount = book.price,
        balance_after_transaction = request.user.account.balance - book.price,
        transaction_type = BORROW,
        timestamp = timezone.now()
    )
    account.balance -= book.price
    account.save(update_fields=['balance',])
    return redirect('profile')

@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.save()
    book.borrower.remove(request.user)
    Transaction.objects.create(
        user = request.user.account,
        amount = book.price,
        balance_after_transaction = request.user.account.balance + book.price,
        transaction_type = RETURN,
        timestamp=timezone.now()
    )
    account = request.user.account
    account.balance += book.price
    account.save(update_fields=['balance',])
    return redirect('profile')
