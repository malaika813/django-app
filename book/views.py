from django.shortcuts import render ,redirect
from .models import Book,Review
from django.views import View
from .forms import ReviewForm


# Create your views here.
def book(request):
    books=Book.objects.all()
    return render (request , 'book.html' ,locals())
    

def detail(request,pk):
    books=Book.objects.get(pk=pk)
    return render(request ,'book_detail.html',locals())


def review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review')   # refresh the page after saving
    else:
        form = ReviewForm()

    reviews = Review.objects.all().order_by('-id')
    return render(request, 'review.html', {'form': form, 'reviews': reviews})