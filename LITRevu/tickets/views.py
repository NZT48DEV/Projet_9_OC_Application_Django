from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from . import forms, models
from tickets.models import Ticket
from tickets.forms import TicketForm, ImageForm
from reviews.models import Review
from userfollows.models import UserBlock  # ✅ pour vérifier les blocages


@login_required
def home(request):
    images = models.Image.objects.all()
    tickets = models.Ticket.objects.all()
    return render(request, 'tickets/home.html', {
        'images': images,
        'tickets': tickets,
        'read_only': True,                   # lecture seule
        'next': request.GET.get("next", ""), # pour naviguer proprement
    })


@login_required
def image_upload(request):
    form = forms.ImageForm()
    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            next_url = request.POST.get("next")
            return redirect(next_url or 'home')
    return render(request, 'tickets/image_upload.html', {
        'form': form,
        'read_only': False,                  # on est en création
        'next': request.GET.get("next", ""),
    })


@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    image_form = forms.ImageForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        image_form = forms.ImageForm(request.POST, request.FILES)
        if ticket_form.is_valid() and image_form.is_valid():
            image = image_form.save(commit=False)
            image.uploader = request.user
            image.save()
            ticket = ticket_form.save(commit=False)
            ticket.image = image
            ticket.user = request.user  # ⚠ champ correct
            ticket.save()
            messages.success(request, "✅ Votre ticket a bien été créé.")
            next_url = request.POST.get("next")
            return redirect(next_url or 'home')
    return render(request, 'tickets/create_ticket.html', {
        'ticket_form': ticket_form,
        'image_form': image_form,
        'read_only': False,                  # on est en création
        'next': request.GET.get("next", ""),
    })


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # ✅ Vérifie si l’auteur du ticket a bloqué l’utilisateur courant
    if UserBlock.objects.filter(user=ticket.user, blocked_user=request.user).exists():
        messages.error(request, "❌ Ce ticket n'est pas disponible.")
        return redirect("home")

    # Toutes les critiques liées à ce ticket
    reviews = Review.objects.filter(ticket=ticket)

    # La critique spécifique de l'utilisateur connecté (s'il en a fait une)
    user_review = reviews.filter(user=request.user).first()

    return render(request, "tickets/view_ticket.html", {
        "ticket": ticket,
        "reviews": reviews,
        "user_review": user_review,
        "hide_ticket": True,                   # tu gardes ta logique
        "read_only": True,                     # page de lecture seule
        "next": request.GET.get("next", ""),   # pour pouvoir revenir facilement
    })


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # ✅ Pas besoin de vérifier blocage ici car seul l'auteur peut supprimer
    if request.method == "POST":
        next_url = request.POST.get("next")  # récupère next du formulaire
        ticket.delete()
        messages.success(request, "✅ Votre ticket a bien été supprimé.")
        return redirect(next_url or "user_posts")  # fallback si pas de next

    return render(request, 'tickets/delete_ticket.html', {
        "ticket": ticket,
        "review": None,                
        "read_only": True,             
        "next": request.GET.get("next", ""),  
    })


@login_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    # ✅ Pas besoin de vérifier blocage ici non plus car seul l'auteur peut modifier
    if request.method == 'POST':
        ticket_form = TicketForm(request.POST, instance=ticket)
        image_form = ImageForm(request.POST, request.FILES, instance=ticket.image)

        if ticket_form.is_valid() and image_form.is_valid():
            # Mise à jour de l'image
            image = image_form.save(commit=False)
            image.uploader = request.user
            image.save()

            # Mise à jour du ticket
            updated_ticket = ticket_form.save(commit=False)
            updated_ticket.image = image
            updated_ticket.save()

            messages.success(request, "✅ Votre ticket a bien été modifié.")
            next_url = request.POST.get("next")
            return redirect(next_url or "view_ticket", ticket_id=updated_ticket.pk)

    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=ticket.image)

    return render(request, 'tickets/update_ticket.html', {
        'ticket_form': ticket_form,
        'image_form': image_form,
        'ticket': ticket,
        "review": None,           # tu gardes ta logique initiale
        "read_only": False,       # important pour tes partials
        "next": request.GET.get("next", ""),  # next pour revenir à la bonne page
    })
