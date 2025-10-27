from django.contrib import admin
from .models import Book,Review

# Register your models here.


@admin.register(Book)
class Admin(admin.ModelAdmin):
    list_display=['title','Author','price']
    

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=['book','review_text','rating']