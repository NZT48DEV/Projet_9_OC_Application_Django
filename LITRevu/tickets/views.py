from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from django.shortcuts import get_object_or_404
from tickets.models import Ticket

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
    ticket = get_object_or_404(models.Ticket, id=ticket_id)
    return render(request, 'tickets/view_ticket.html', {'ticket': ticket})

@login_required
def delete_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)

    if request.method == "POST":
        ticket.delete()
        return redirect('home')

    return render(request,
                  'tickets/delete_ticket.html', 
                  {'ticket': ticket})