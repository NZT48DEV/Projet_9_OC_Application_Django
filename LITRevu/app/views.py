from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models
from django.shortcuts import get_object_or_404

@login_required
def home(request):
    photos = models.Photo.objects.all()
    tickets = models.App.objects.all()
    return render(request, 'app/home.html', context={'photos': photos, 'tickets': tickets})

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
    return render(request, 'app/photo_upload.html', context={'form': form})

@login_required
def ticket_create(request):
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
    return render(request, 'app/create_ticket.html', context=context)

@login_required
def view_ticket(request, ticket_id):
    ticket = get_object_or_404(models.App, id=ticket_id)
    return render(request, 'app/view_ticket.html', {'ticket': ticket})