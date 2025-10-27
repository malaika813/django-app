
from django.urls import path,include
from . import views
from django.views import View
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('book/',views.book,name='book'),
    path('book_detail/<int:pk>',views.detail,name='book_detail'),
    path('review/',views.review,name='review'),
    
]

