from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from .forms import ReviewForm
from reviews.models import Review

@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'reviews/view_review.html', {'review': review})

@login_required
def create_review(request, review_id=None):
    review = None
    if review_id:
        review = get_object_or_404(review, id=review_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user  # l’utilisateur connecté est l’auteur
            review.save()
            return redirect('home')  # redirige vers la page d’accueil
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'review': review,
    }
    return render(request, 'reviews/create_review.html', context)


@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == "POST":
        review.delete()
        return redirect('home')

    return render(request,
                  'reviews/delete_review.html', 
                  {'review': review})