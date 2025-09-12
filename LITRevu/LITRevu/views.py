from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tickets.models import Ticket
from reviews.models import Review

@login_required
def home(request):
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(request, 'LITRevu/home.html', {
        'tickets': tickets,
        'reviews': reviews
    })
