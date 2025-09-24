from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from . import forms, models
from tickets.models import Ticket, Image
from tickets.forms import TicketForm, ImageForm
from reviews.models import Review
from userfollows.models import UserBlock  # ✅ pour vérifier les blocages


@login_required
def home(request):
    tickets = Ticket.objects.all()
    return render(request, "tickets/home.html", {
        "tickets": tickets,
        "read_only": True,
    })


@login_required
def image_upload(request):
    form = forms.ImageForm()
    if request.method == "POST":
        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            messages.success(request, "✅ Image téléchargée avec succès.")
            return redirect("home")
    return render(request, "tickets/image_upload.html", {
        "form": form,
        "read_only": False,
    })


@login_required
def create_ticket(request):
    ticket_form = TicketForm()
    image_form = ImageForm()
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        if ticket_form.is_valid() and image_form.is_valid():
            # Création du ticket
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()

            # Création de l’image liée (si uploadée)
            if image_form.cleaned_data.get("image"):
                image = image_form.save(commit=False)
                image.uploader = request.user
                image.ticket = ticket
                image.save()

            messages.success(request, "✅ Votre ticket a bien été créé.")
            return redirect("home")
    return render(request, "tickets/create_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "read_only": False,
    })


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # ✅ Vérifie si l’auteur du ticket a bloqué l’utilisateur courant
    if UserBlock.objects.filter(user=ticket.user, blocked_user=request.user).exists():
        messages.error(request, "❌ Ce ticket n'est pas disponible.")
        return redirect("home")

    reviews = Review.objects.filter(ticket=ticket)
    user_review = reviews.filter(user=request.user).first()

    return render(request, "tickets/view_ticket.html", {
        "ticket": ticket,
        "reviews": reviews,
        "user_review": user_review,
        "hide_ticket": True,
        "read_only": True,
    })


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == "POST":
        ticket.delete()
        messages.success(request, "✅ Votre ticket a bien été supprimé.")
        return redirect("home")

    return render(request, "tickets/delete_ticket.html", {
        "ticket": ticket,
        "review": None,
        "read_only": True,
    })


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # ✅ Vérifie si une image existe déjà
    try:
        image_instance = ticket.image
    except Image.DoesNotExist:
        image_instance = None

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(request.POST, request.FILES, instance=image_instance)

        if ticket_form.is_valid() and image_form.is_valid():
            # Mise à jour du ticket
            updated_ticket = ticket_form.save(commit=False)
            updated_ticket.user = request.user
            updated_ticket.save()

            # Mise à jour ou création de l’image
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

    return render(request, "tickets/update_ticket.html", {
        "ticket_form": ticket_form,
        "image_form": image_form,
        "ticket": ticket,
        "review": None,
        "read_only": False,
    })
