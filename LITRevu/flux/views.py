from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tickets.models import Ticket
from reviews.models import Review


# Create your views here.
@login_required
def home(request):
    tickets = Ticket.objects.all().select_related("user").prefetch_related("review_set")

    # IDs des tickets déjà critiqués par l’utilisateur courant
    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    return render(request, "flux/home.html", {
        "tickets": tickets,
        "reviewed_ticket_ids": reviewed_ticket_ids
    })
