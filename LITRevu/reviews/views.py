"""
Vues pour la gestion des critiques (reviews).
Inclut la création, la mise à jour, la suppression, ainsi que la gestion conjointe
ticket + critique.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from reviews.forms import ReviewForm
from reviews.models import Review
from tickets.forms import ImageForm, TicketForm
from tickets.models import Image, Ticket
from userfollows.models import UserBlock


@login_required
def view_review(request, review_id):
    """
    Affiche une critique spécifique.
    - Vérifie si l’auteur du ticket lié a bloqué l’utilisateur courant.
    - Si bloqué → redirige avec message d’erreur.
    """
    review = get_object_or_404(Review, id=review_id)

    if UserBlock.objects.filter(
        user=review.ticket.user, blocked_user=request.user
    ).exists():
        messages.error(request, "❌ Cette critique n'est pas disponible.")
        return redirect("home")

    return render(
        request,
        "reviews/view_review.html",
        {
            "review": review,
            "read_only": True,
        },
    )


@login_required
def create_review_with_ticket(request):
    """
    Crée une critique en même temps qu’un ticket.
    - Valide et sauvegarde TicketForm, ImageForm et ReviewForm.
    - Associe le ticket et la critique à l’utilisateur courant.
    """
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        review_form = ReviewForm(request.POST)

        if (
            ticket_form.is_valid()
            and image_form.is_valid()
            and review_form.is_valid()
        ):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(
                request, "✅ Votre ticket et critique ont bien été créés."
            )
            return redirect("home")
    else:
        ticket_form = TicketForm()
        image_form = ImageForm()
        review_form = ReviewForm()

    return render(
        request,
        "reviews/create_review_with_ticket.html",
        {
            "ticket_form": ticket_form,
            "image_form": image_form,
            "review_form": review_form,
        },
    )


@login_required
def create_review_response(request, ticket_id):
    """
    Crée une critique en réponse à un ticket existant.
    - Vérifie si l’auteur du ticket a bloqué l’utilisateur courant.
    - Empêche la création si une critique existe déjà pour ce ticket.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if UserBlock.objects.filter(
        user=ticket.user, blocked_user=request.user
    ).exists():
        messages.error(request, "❌ Vous ne pouvez pas répondre à ce ticket.")
        return redirect("home")

    if Review.objects.filter(ticket=ticket).exists():
        messages.error(request, "❌ Ce ticket a déjà une critique.")
        return redirect("home")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            messages.success(request, "✅ Votre critique a bien été publiée.")
            return redirect("view_ticket", ticket_id=ticket.pk)
    else:
        form = ReviewForm()

    return render(
        request,
        "reviews/create_review_response.html",
        {
            "ticket": ticket,
            "review_form": form,
        },
    )


@login_required
def delete_review(request, review_id):
    """
    Supprime une critique (si l’utilisateur en est l’auteur).
    - Si méthode POST → suppression directe et redirection vers user_posts.
    - Sinon → affiche confirmation.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "✅ Votre critique a bien été supprimée.")
        return redirect("user_posts")

    return render(request, "reviews/delete_review.html", {"review": review})


@login_required
def update_review(request, review_id):
    """
    Met à jour une critique existante (si l’utilisateur en est l’auteur).
    - Préremplit le formulaire avec les données de la critique.
    - Sauvegarde les modifications si formulaire valide.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Votre critique a bien été modifiée.")
            return redirect("view_review", review_id=review.pk)
    else:
        form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/update_review.html",
        {
            "form": form,
            "review": review,
        },
    )


@login_required
def update_review_with_ticket(request, review_id):
    """
    Met à jour une critique et son ticket associé.
    - Permet aussi de supprimer soit la critique, soit le ticket via POST.
    - Met à jour TicketForm, ImageForm et ReviewForm ensemble.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    try:
        image_instance = ticket.image
    except Image.DoesNotExist:
        image_instance = None

    if request.method == "POST":
        if "delete_review" in request.POST:
            review.delete()
            messages.success(
                request, "✅ Votre critique a bien été supprimée."
            )
            return redirect("user_posts")

        if "delete_ticket" in request.POST:
            ticket.delete()
            messages.success(request, "✅ Votre ticket a bien été supprimé.")
            return redirect("user_posts")

        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(
            request.POST, request.FILES, instance=image_instance
        )
        review_form = ReviewForm(request.POST, instance=review)

        if (
            ticket_form.is_valid()
            and image_form.is_valid()
            and review_form.is_valid()
        ):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            messages.success(
                request, "✅ Vos modifications ont bien été enregistrées."
            )
            return redirect("view_review", review_id=review.pk)
    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=image_instance)
        review_form = ReviewForm(instance=review)

    return render(
        request,
        "reviews/update_review_with_ticket.html",
        {
            "ticket_form": ticket_form,
            "image_form": image_form,
            "review_form": review_form,
            "ticket": ticket,
            "review": review,
        },
    )


@login_required
def delete_review_with_ticket(request, review_id):
    """
    Supprime une critique et son ticket associé (si l’utilisateur en est l’auteur).
    - Si méthode POST → suppression des deux objets, puis redirection.
    - Sinon → affiche confirmation.
    """
    review = get_object_or_404(Review, id=review_id, user=request.user)
    ticket = review.ticket

    if request.method == "POST":
        review.delete()
        ticket.delete()
        messages.success(
            request, "✅ Le ticket et sa critique ont bien été supprimés."
        )
        return redirect("user_posts")

    return render(
        request,
        "reviews/delete_review_with_ticket.html",
        {
            "review": review,
            "ticket": ticket,
        },
    )
