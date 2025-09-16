from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from django.shortcuts import get_object_or_404
from tickets.models import Ticket
from tickets.forms import TicketForm, ImageForm
from reviews.models import Review

@login_required
def home(request):
    images = models.Image.objects.all()
    tickets = models.Ticket.objects.all()
    return render(request, 'tickets/home.html', context={'images': images, 'tickets': tickets})

@login_required
def image_upload(request):
    form = forms.ImageForm()
    if request.method == 'POST':
        form = forms.ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.uploader = request.user
            image.save()
            return redirect('home')
    return render(request, 'tickets/image_upload.html', context={'form': form})

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
            ticket.user = request.user  # ⚠ pas ticket.author, ton champ s'appelle user
            ticket.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'image_form': image_form,
    }
    return render(request, 'tickets/create_ticket.html', context=context)


@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    user_review = Review.objects.filter(ticket=ticket, user=request.user).first()
    return render(request, "tickets/view_ticket.html", {
        "ticket": ticket,
        "review": user_review,  # critique de l’utilisateur connecté
    })


@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        ticket.delete()
        return redirect('home')

    return render(request,
                  'tickets/delete_ticket.html', 
                  {'ticket': ticket})


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

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

            return redirect('view_ticket', ticket_id=updated_ticket.pk)  # <-- pk sûr
    else:
        ticket_form = TicketForm(instance=ticket)
        image_form = ImageForm(instance=ticket.image)

    return render(request, 'tickets/update_ticket.html', {
        'ticket_form': ticket_form,
        'image_form': image_form,
        'ticket': ticket,   # utile si tu veux afficher titre ou id dans le template
    })
