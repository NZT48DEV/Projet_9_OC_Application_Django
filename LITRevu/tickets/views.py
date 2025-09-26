"""
Vues pour la gestion des tickets et des images associées.
Inclut la création, la modification, la visualisation et la suppression.
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from reviews.models import Review
from tickets.forms import ImageForm, TicketForm
from tickets.models import Image, Ticket
from userfollows.models import UserBlock

from . import forms


@login_required
def image_upload(request):
    """
    Permet à l’utilisateur d’uploader une image.
    - Si méthode POST → sauvegarde l’image avec l’utilisateur courant comme uploader.
    - Redirige ensuite vers la home avec un message de succès.
    """
    form = forms.ImageForm()
    if request.method == "POST":
        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            messages.success(request, "✅ Image téléchargée avec succès.")
            return redirect("home")

    return render(
        request,
        "tickets/image_upload.html",
        {
            "form": form,
            "read_only": False,
        },
    )


@login_required
def create_ticket(request):
    """
    Création d’un nouveau ticket avec option d’ajout d’une image.
    - Valide les formulaires TicketForm et ImageForm.
    - Associe le ticket et l’image à l’utilisateur courant.
    """
    ticket_form = TicketForm()
    image_form = ImageForm()

    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)

        if ticket_form.is_valid() and image_form.is_valid():
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            messages.success(request, "✅ Votre ticket a bien été créé.")
            return redirect("home")

    return render(
        request,
        "tickets/create_ticket.html",
        {
            "ticket_form": ticket_form,
            "image_form": image_form,
            "read_only": False,
        },
    )


@login_required
def view_ticket(request, ticket_id):
    """
    Affiche le détail d’un ticket spécifique.
    - Vérifie si l’auteur du ticket a bloqué l’utilisateur courant.
    - Récupère toutes les critiques associées.
    - Passe la première critique de l’utilisateur courant séparément.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if UserBlock.objects.filter(
        user=ticket.user, blocked_user=request.user
    ).exists():
        messages.error(request, "❌ Ce ticket n'est pas disponible.")
        return redirect("home")

    reviews = Review.objects.filter(ticket=ticket)
    user_review = reviews.filter(user=request.user).first()

    return render(
        request,
        "tickets/view_ticket.html",
        {
            "ticket": ticket,
            "reviews": reviews,
            "user_review": user_review,
            "hide_ticket": True,
            "read_only": True,
        },
    )


@login_required
def delete_ticket(request, ticket_id):
    """
    Supprime un ticket (uniquement si l’utilisateur courant en est l’auteur).
    - Si méthode POST → suppression du ticket puis redirection home.
    - Si méthode GET → affiche une page de confirmation.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "✅ Votre ticket a bien été supprimé.")
        return redirect("home")

    return render(
        request,
        "tickets/delete_ticket.html",
        {
            "ticket": ticket,
            "review": None,
            "read_only": True,
        },
    )


@login_required
def update_ticket(request, ticket_id):
    """
    Met à jour un ticket existant (uniquement si l’utilisateur en est l’auteur).
    - Préremplit les formulaires TicketForm et ImageForm avec les données existantes.
    - Si méthode POST → enregistre les modifications du ticket et de son image associée.
    """
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    try:
        image_instance = ticket.image
    except Image.DoesNotExist:
        image_instance = None

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(
            request.POST, request.FILES, instance=image_instance
        )

        if ticket_form.is_valid() and image_form.is_valid():
            updated_ticket = ticket_form.save(commit=False)
            updated_ticket.user = request.user
            updated_ticket.save()

            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = updated_ticket
                image.save()

            messages.success(request, "✅ Votre ticket a bien été modifié.")
            return redirect("view_ticket", ticket_id=updated_ticket.pk)
    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=image_instance)

    return render(
        request,
        "tickets/update_ticket.html",
        {
            "ticket_form": ticket_form,
            "image_form": image_form,
            "ticket": ticket,
            "review": None,
            "read_only": False,
        },
    )
