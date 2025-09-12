from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from django.shortcuts import get_object_or_404
from tickets.models import Ticket

@login_required
def home(request):
    photos = models.Photo.objects.all()
    tickets = models.Ticket.objects.all()
    return render(request, 'tickets/home.html', context={'photos': photos, 'tickets': tickets})

@login_required
def photo_upload(request):
    form = forms.PhotoForm()
    if request.method == 'POST':
        form = forms.PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            # set the uploader to the user before saving the model
            photo.uploader = request.user
            # now we can save
            photo.save()
            return redirect('home')
    return render(request, 'tickets/photo_upload.html', context={'form': form})

@login_required
def create_ticket(request):
    ticket_form = forms.TicketForm()
    photo_form = forms.PhotoForm()
    if request.method == 'POST':
        ticket_form = forms.TicketForm(request.POST)
        photo_form = forms.PhotoForm(request.POST, request.FILES)
        if any([ticket_form.is_valid(), photo_form.is_valid()]):
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()
            ticket = ticket_form.save(commit=False)
            ticket.photo = photo
            ticket.author = request.user
            ticket.save()
            return redirect('home')
    context = {
        'ticket_form': ticket_form,
        'photo_form': photo_form,
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