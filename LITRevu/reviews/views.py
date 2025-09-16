from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import models
from .forms import ReviewForm
from reviews.models import Review

@login_required
def view_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id)
    return render(request, 'reviews/view_review.html', {'review': review})

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from tickets.forms import TicketForm, ImageForm
from tickets.models import Ticket
from .forms import ReviewForm


@login_required
def create_review_with_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)
        if ticket_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("home")
    else:
        ticket_form = TicketForm()
        review_form = ReviewForm()
    return render(request, "reviews/create_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "review_form": review_form
    })

@login_required
def create_review_response(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Vérifier si l’utilisateur a déjà une critique
    if Review.objects.filter(ticket=ticket, user=request.user).exists():
        return redirect("view_ticket", ticket.id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("view_ticket", ticket.id)
    else:
        form = ReviewForm()
    return render(request, "reviews/create_review_response.html", {
        "ticket": ticket,
        "review_form": form
    })
@login_required
def delete_review(request, review_id):
    review = Review.objects.get(id=review_id)

    if request.method == "POST":
        review.delete()
        return redirect('home')

    return render(request,
                  'reviews/delete_review.html', 
                  {'review': review})

@login_required
def update_review(request, review_id):
    review = get_object_or_404(models.Review, id=review_id, user=request.user)  # idem, sécurité
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('view_review', review_id=review.id)
    else:
        form = ReviewForm(instance=review)

    return render(request, 'reviews/update_review.html', {'form': form, 'review': review})
