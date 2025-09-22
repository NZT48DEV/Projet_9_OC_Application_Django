from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from tickets.models import Ticket
from reviews.models import Review
from userfollows.models import UserFollows, UserBlock


@login_required
def home(request):
    # Si un paramètre est présent dans l’URL → mettre à jour la session
    if "filter" in request.GET:
        request.session["filter_mode"] = request.GET["filter"]

    # Sinon → utiliser la valeur en session (ou "following" par défaut)
    filter_mode = request.session.get("filter_mode", "following")

    # 🔹 Récupère les utilisateurs qui m’ont bloqué
    blocked_me = UserBlock.objects.filter(
        blocked_user=request.user
    ).values_list("user_id", flat=True)

    if filter_mode == "all":
        tickets = Ticket.objects.exclude(user_id__in=blocked_me)
    else:  # filter_mode == "following"
        followed_users = UserFollows.objects.filter(
            user=request.user
        ).values_list("followed_user", flat=True)

        tickets = Ticket.objects.filter(
            user__in=list(followed_users) + [request.user.id]
        ).exclude(user_id__in=blocked_me)

    tickets = (
        tickets.select_related("user")
        .prefetch_related("review_set")
        .order_by("-time_created")
    )

    reviewed_ticket_ids = set(
        Review.objects.filter(user=request.user).values_list("ticket_id", flat=True)
    )

    return render(request, "flux/home.html", {
        "tickets": tickets,
        "reviewed_ticket_ids": reviewed_ticket_ids,
        "filter_mode": filter_mode,
    })
