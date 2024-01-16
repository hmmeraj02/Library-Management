from django.db import models
from category.models import Category
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=20)
    author = models.CharField(max_length=30)
    description = models.TextField()
    genre = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='book/media/uploads/')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    borrower = models.ManyToManyField(User, blank=True)

    def __str__(self) -> str:
        return self.title
    
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review by {self.name}"