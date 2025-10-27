from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Book(models.Model):
    book_id=models.AutoField
    title=models.CharField(max_length=50)
    Author=models.CharField(max_length=50)
    price=models.DecimalField( max_digits=7,decimal_places=2)
    
    def __str__(self):
        return self.title
    
    


class Review(models.Model):
    book=models.ForeignKey(Book, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=100,null=True, blank=True, default="Anonymous") 

    review_text=models.TextField()
    rating=models.IntegerField()
    
    def __str__(self):
        return f"Review for {self.book.title} by {self.author.username} - Rating: {self.rating}"

