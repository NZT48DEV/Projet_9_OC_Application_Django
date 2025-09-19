from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from tickets.forms import TicketForm, ImageForm
from reviews.forms import ReviewForm
from reviews.models import Review
from tickets.models import Ticket


@login_required
def view_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    return render(request, 'reviews/view_review.html', {'review': review})


@login_required
def create_review_with_ticket(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if ticket_form.is_valid() and image_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.save()
                ticket.image = image

            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            next_url = request.POST.get("next")
            return redirect(next_url or "home")
    else:
        ticket_form = TicketForm()
        image_form = ImageForm()
        review_form = ReviewForm()

    return render(request, "reviews/create_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "review_form": review_form,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
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

            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")
    else:
        form = ReviewForm()

    return render(request, "reviews/create_review_response.html", {
        "ticket": ticket,
        "review_form": form,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        next_url = request.POST.get("next")
        review.delete()
        messages.success(request, "✅ Votre critique a bien été supprimée.")
        return redirect(next_url or "user_posts")

    return render(request, "reviews/delete_review.html", {
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def update_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Votre critique a bien été modifiée.")

            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")
    else:
        form = ReviewForm(instance=review)

    return render(request, "reviews/update_review.html", {
        "form": form,
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def update_review_with_ticket(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        if "delete_review" in request.POST:
            review.delete()
            messages.success(request, "✅ Votre critique a bien été supprimée.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")

        if "delete_ticket" in request.POST:
            ticket.delete()
            messages.success(request, "✅ Votre ticket a bien été supprimé.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")

        # Sinon → bouton Enregistrer
        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(request.POST, request.FILES, instance=ticket.image if ticket.image else None)
        review_form = ReviewForm(request.POST, instance=review)

        if ticket_form.is_valid() and image_form.is_valid() and review_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.save()
                ticket.image = image

            ticket.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(request, "✅ Vos modifications ont bien été enregistrées.")
            next_url = request.POST.get("next")
            return redirect(next_url or "user_posts")
    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=ticket.image if ticket.image else None)
        review_form = ReviewForm(instance=review)

    return render(request, "reviews/update_review_with_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "review_form": review_form,
        "ticket": ticket,
        "review": review,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })


@login_required
def delete_review_with_ticket(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        next_url = request.POST.get("next")
        review.delete()
        ticket.delete()
        messages.success(request, "✅ Le ticket et sa critique ont bien été supprimés.")
        return redirect(next_url or "user_posts")

    return render(request, "reviews/delete_review_with_ticket.html", {
        "review": review,
        "ticket": ticket,
        "next": request.GET.get("next", request.META.get("HTTP_REFERER", "")),
    })
