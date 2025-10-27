from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['book', 'author_name', 'review_text', 'rating']
        widgets = {
            'book': forms.Select(attrs={'class': 'form-control'}),
            'author_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your name'}),
            'review_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Write your review...'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }
