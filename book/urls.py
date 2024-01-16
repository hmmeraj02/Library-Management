from django.urls import path
from . import views
urlpatterns = [
    path('book_detail/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('borrow_book/<int:pk>/', views.borrow_book, name='borrow_book'),
    path('return_book/<int:pk>/', views.return_book, name='return_book'),
    path('review_book/<int:pk>/', views.add_review, name='review_book'),
]