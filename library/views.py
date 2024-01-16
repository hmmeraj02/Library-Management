from django.shortcuts import render
from book.models import Book
from category.models import Category

def home(request, category_slug=None):
    books = Book.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug=category_slug)
        books = Book.objects.filter(genre=category)
    categories = Category.objects.all()
    return render(request, 'index.html', {'book': books, 'category': categories})